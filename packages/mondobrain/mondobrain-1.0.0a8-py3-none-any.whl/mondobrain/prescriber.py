from io import BytesIO
import time

import numpy as np
import pandas as pd

from mondobrain import utilities
from mondobrain.core.frame import MondoDataFrame
from mondobrain.core.series import MondoSeries


class SolveRequestError(Exception):
    pass


class StatusRequestError(Exception):
    pass


class Solver:
    """
    MondoBrain Solver object.

    Applies a stochastic search for the global maximum Z-score with respect to
    a defined dependent variable and target class, in cases of "discrete" variables
    or target min/max mean in the cases of "continuous" variables.

    Parameters
    ----------
    client: client
        The client class that you configured in a previous step

    min_size_frac: float (optional), default=0.2
        Value between 0.0 and 1.0 that defines the minimum number of points needed
        for a valid rule discovered by the MondoBrain solver.

    min_purity: float (optional), default=0.0
        Value between 0.0 and 1.0 that defines the minimum purity needed for a
        valid rule discovered by the MondoBrain solver.

        Purity here is defined as the mean of the target variable distribution.

    max_cycles: int (optional), default=90
        Value greater than 0 that defines the total cycles the MondoBrain solver
        should commit in order to find a valid rule.

    api_key: str (optional), default=None
        In order to make a Solver.fit() API request, an API Token/Key is required.
        Please contact a MondoBrain account manager to receive a token.

    Methods
    ----------
    fit(self, X, y)

    Examples
    ----------
    >>> from mondobrain.prescriber import Solver
    ...
    >>> solver = Solver(api_key='8d9ed389-4e27-41f9-a831-f295207af7d')
    >>> solver.fit(mdf_explorable, mdf_outcome)
    >>> solver.rule
    {'sex': {'low': 'male', 'high': 'male'},
     'class': {'low': 2, 'high': 3},
     'parch': {'low': 0, 'high': 0},
     'ticketnumber': {'low': 2152.0, 'high': 3101281.0}}
    >>> solver.score
    12.974682681486312
    """

    def __init__(self, client, min_size_frac=0.2, min_purity=0.0, max_cycles=90):
        self.client = client
        self.min_size_frac = min_size_frac
        self.min_purity = min_purity
        self.max_cycles = max_cycles

    @staticmethod
    def _is_one_dim_solve(explorable_vars):
        return explorable_vars.shape[1] == 1

    @staticmethod
    def _get_time_out(
        explorable_vars, lg_timeout_coefficient=3.5, max_outer_loop_timeout=90
    ):
        number_of_points = explorable_vars.shape[0]
        number_of_active_vars = explorable_vars.shape[1]
        min_timeout = np.minimum(
            int(
                lg_timeout_coefficient
                * np.sqrt(number_of_points * number_of_active_vars / 2)
            ),
            max_outer_loop_timeout,
        )

        timeout = np.maximum(1, min_timeout)

        return timeout

    @staticmethod
    def _bin_dataframe(dataset=None):
        buffer = BytesIO()
        dataset.to_parquet(buffer)

        return buffer.getvalue()

    def _request_solve(self, dataframe=None, serialized_params=None):
        bin_dataset = Solver._bin_dataframe(dataframe)

        files = {"file": ("dataset.parquet", bin_dataset, "text/plain")}

        params_to_keep = [
            "outcome",
            "outcome_target",
            "min_rule_size_pct",
            "time_out",
            "case_point_dict",
        ]
        solve_params = {
            key: val for key, val in serialized_params.items() if key in params_to_keep
        }

        return self.client._solver.post(data=solve_params, files=files)

    def _request_status(self, task_id):
        return self.client._solver.status.post(data={"task_id": task_id})

    def _run_solver(self, serialized_params=None, dataframe=None):
        solve_finished = False

        solve_response = self._request_solve(
            dataframe=dataframe, serialized_params=serialized_params,
        )

        if solve_response.status_code != 200:
            raise SolveRequestError(
                f"Error in requesting Solve: {solve_response.status_code}"
            )

        solve_content = solve_response.json()
        if "task_id" in solve_content.keys():
            if solve_content["state"] == "SUCCESS":
                return solve_content["result"]
            elif solve_content["state"] == "FAILURE":
                raise StatusRequestError("Something went wrong during Solve.")
            else:
                while not solve_finished:
                    task_id = solve_content["task_id"]
                    status_response = self._request_status(task_id)

                    status_content = status_response.json()
                    if status_content["state"] == "SUCCESS":
                        solve_finished = True
                    elif status_content["state"] == "FAILURE":
                        raise StatusRequestError(status_content["result"])
                    else:
                        time.sleep(5)
                        continue

                return status_content["result"]
        else:
            return solve_content

    @property
    def max_cycles(self):
        return self._max_cycles

    @max_cycles.setter
    def max_cycles(self, value):
        if value > 0:
            self._max_cycles = value
        else:
            raise ValueError("'max_cycles' must be greater than 0.")

    def fit(self, m_X, m_y):
        """
            Fit the Solver with the provided data.

            Parameters
            ----------
            m_X: MondoDataFrame of shape (n_samples, n_features)
                Where n_samples is the number of samples and n_features is the
                number of features.

            m_y: MondoSeries of shape (n_samples,)
                Where n_samples is the number of samples and aligns with
                n_samples of m_X.
        """
        params = dict()
        params["outcome"] = m_y.name
        params["outcome_target"] = m_y.target_class
        params["one_dim_solve"] = self._is_one_dim_solve(explorable_vars=m_X)
        params["time_out"] = self._get_time_out(
            explorable_vars=m_X, max_outer_loop_timeout=self.max_cycles
        )
        params["min_rule_size_pct"] = self.min_size_frac
        params["case_point_dict"] = {
            var: ms.case_point
            for var, ms in m_X.iteritems()
            if ms.case_point is not None
        }
        mdf = MondoDataFrame(pd.concat((MondoDataFrame(m_y), m_X), axis=1))
        self.encoding_map = utilities.DDTransformer(mdf)

        edf = utilities.encode_dataframe(mdf, self.encoding_map)

        if m_y.var_type == "discrete":
            target_class_to_use = utilities.encode_column(
                MondoSeries([m_y.target_class], name=m_y.name), self.encoding_map
            )[0]
        else:
            target_class_to_use = m_y.target_class

        outcome_to_use = self.encoding_map.original_to_encoded(m_y.name, m_y)[1]

        df, was_sampled = utilities.sample_if_needed(
            edf, target_class=target_class_to_use, target_variable=outcome_to_use
        )

        params["outcome"] = outcome_to_use
        params["outcome_target"] = target_class_to_use
        result_dict = self._run_solver(params, df)

        for key, item in result_dict.items():
            setattr(self, key, item)

        self.real_values = utilities.decode_rule(self.encoded_values, self.encoding_map)

        if m_y.var_type == "discrete":
            stat_values = self.real_values
            stat_df = mdf
            target_class_to_use = m_y.target_class
            outcome_to_use = m_y.name
        else:
            stat_values = self.encoded_values
            stat_df = edf

        sample_stats = utilities.get_stats_dict(
            utilities.apply_rule_to_db(stat_df, stat_values),
            target_class=target_class_to_use,
            target_variable=outcome_to_use,
        )

        self.score = utilities.score_rule(
            stat_df, stat_values, target_class_to_use, outcome_to_use
        )
        self.size = sample_stats["size"]
        self.mean = sample_stats["mean"]
        self.rule = utilities.prettify_rule(self.real_values, mdf)
