from collections import defaultdict
import string

import numpy as np
from sklearn.preprocessing import LabelEncoder

from mondobrain.core.frame import MondoDataFrame
from mondobrain.core.series import MondoSeries


def encode_column(dataseries, encoder):
    encoded, encoded_col_label = encoder.original_to_encoded(
        dataseries.name, dataseries
    )
    ms_encoded = MondoSeries(encoded, name=encoded_col_label)

    # Need to change encoded nulls back to nulls
    ms_encoded.where(~dataseries.reset_index(drop=True).isnull(), np.nan, inplace=True)

    return ms_encoded


def encode_dataframe(dataframe, encoder):
    """
    DOCSTRING
    :return: encoded MondoDataFrame,
    """
    encoded_dict = dict()

    for column, values in dataframe.iteritems():
        encoded_col = encode_column(values, encoder)
        encoded_dict[encoded_col.name] = encoded_col

    encoded_dataframe = MondoDataFrame.from_dict(encoded_dict)

    return encoded_dataframe


def decode_column(dataseries, decoder):
    numeric_col_label = decoder._column_decoder[dataseries.name]
    ms_decoded = decoder.encoded_to_original(numeric_col_label, dataseries)

    return ms_decoded


def decode_dataframe(dataframe, decoder):
    decoded_dict = dict()
    for col, ser in dataframe.iteritems():
        decoded_dict[col] = decode_column(ser, decoder)

    return MondoDataFrame.from_dict(decoded_dict)


def clean_nulls(dataseries):
    """
    Function operates on a column and transforms nulls to a base type reference.
    This is required because null or NaN types are generally float distinct
    float values and will be encoded distinctly otherwise
    :param dataseries:
    :return:
    """
    clean_me = dataseries.copy()

    # these values will be used as replacement values
    # to ensure that they float to the top
    min_int = np.iinfo(np.int64).min
    min_float = np.finfo(np.float64).min
    min_str = "      "

    # define a dict with objects to replace nulls
    the_cleaner = ((np.object_, min_str), (np.int64, min_int), (np.float64, min_float))

    # run pd.fillna replacements with each of the columns
    # sets and fill according to type
    for obj, base in the_cleaner:
        if np.issubdtype(clean_me.dtype, obj):
            clean_me.fillna(base, inplace=True)

    return clean_me


def sample_if_needed(df, target_class, target_variable):

    SAMPLING_SIZE = 2500
    SAMPLING_CAP = 3500

    if df.shape[0] > SAMPLING_CAP:

        was_sampled = True

        # if the outcome is not numeric, we might use oversampled outcomes and
        # the total number of points are less than 0.15 of the overall
        if not np.issubdtype(df[target_variable], np.number):
            if df[target_variable].value_counts()[target_class] / df.shape[0] < 0.15:
                # If they are, we will over sample them
                df = oversampled_result(
                    df, target_variable, target_class, SAMPLING_SIZE
                )
            elif df[target_variable].value_counts().shape[0] == 2:
                target_classes = df[target_variable].value_counts().index
                alternate_class = target_classes[
                    ~np.in1d(target_classes, target_class)
                ][0]
                if (
                    df[target_variable].value_counts()[alternate_class] / df.shape[0]
                    < 0.15
                ):
                    # If they are, we will over sample them
                    df = oversampled_result(
                        df, target_variable, alternate_class, SAMPLING_SIZE
                    )
                else:
                    df = df.sample(SAMPLING_SIZE, random_state=1337).reset_index(
                        drop=True
                    )
            else:
                df = df.sample(SAMPLING_SIZE, random_state=1337).reset_index(drop=True)
        else:
            df = df.sample(SAMPLING_SIZE, random_state=1337).reset_index(drop=True)

    else:
        was_sampled = False

    return df, was_sampled


def oversampled_result(df, outcome, target_class, sampling_size):
    target_prob = 1 - (df[outcome] == target_class).sum() / df.shape[0]
    opposing_prob = 1 - target_prob
    pick_probabilities = np.where(
        df[outcome] == target_class, target_prob, opposing_prob
    )
    pick_probabilities = pick_probabilities / pick_probabilities.sum()
    # this sampling approach will choose every value of the underrepresented
    # class until they are all chosen
    df_sample = df.sample(
        sampling_size, random_state=1337, weights=pick_probabilities
    ).reset_index(drop=True)
    return df_sample


def decode_rule(encoded_rule, encoding_map):
    real_vals = dict()
    for col, val in encoded_rule.items():
        decoded_col = encoding_map._column_decoder[col]
        decoded_val = MondoSeries(list(val.values()))
        decoded_rule = encoding_map.encoded_to_original(decoded_col, decoded_val)
        decoded_bounds = decoded_rule.values.tolist()
        original_col = decoded_rule.name
        decoded_dict = dict(zip(["low", "high"], decoded_bounds))
        real_vals[original_col] = decoded_dict

    return real_vals


def apply_rule_to_db(df, mb_rule):
    """
    fn that enables applying a rule learned on another database
    onto a database with the same column names

    rule: format {variable: {'low': low_value, 'high': high_value}}
    """

    def get_mask(df, mb_rule):
        column_name = mb_rule[0]
        conditions = mb_rule[1]
        if conditions["low"] == conditions["high"]:
            # in the case where we have a discrete variable this will be true
            filt = df[column_name] == conditions["low"]
        else:
            try:
                filt = (df[column_name] >= conditions["low"]) & (
                    df[column_name] <= conditions["high"]
                )
            except TypeError:
                raise TypeError(
                    """Attempted to apply a numerical condition to a
                        non-numerical dataframe column"""
                )
        return filt

    combined_mask = np.all(
        np.array([get_mask(df, mb_r) for mb_r in mb_rule.items()]), axis=0
    )
    return df[combined_mask]


def get_stats_dict(dataset, target_class, target_variable):
    stats_dict = {}
    if dataset[target_variable].dtype == np.object:
        values = (dataset[target_variable] == target_class).astype(np.int)
    else:
        values = dataset[target_variable]
        if target_class == "min":
            values *= -1
    stats_dict["mean"] = values.mean()
    stats_dict["std"] = values.std()
    stats_dict["size"] = int(values.size)
    stats_dict["size_above_mean"] = 0
    if values.mean() > 0:
        stats_dict["size_above_mean"] = int((values >= values.mean()).sum())

    return stats_dict


def score_rule(dataset, rule, target_class, target_variable):
    pop_stats = get_stats_dict(dataset, target_class, target_variable)
    df_rule = apply_rule_to_db(dataset, rule)
    sample_stats = get_stats_dict(df_rule, target_class, target_variable)

    score = (
        np.sqrt(sample_stats["size"])
        * (sample_stats["mean"] - pop_stats["mean"])
        / pop_stats["std"]
    )

    return score


def prettify_rule(ugly_rule, dataset):
    pretty_rule = dict()
    for col, bounds in ugly_rule.items():
        if dataset[col].var_type == "discrete":
            pretty_rule[col] = {"discrete": bounds["low"]}
        else:
            pretty_rule[col] = bounds

    return pretty_rule


class DDTransformer:
    """
    -------------------------------------------------
    # A convenience class to access the default dict for
    #  transforming the values to the encoded values and back
    #Example Usage:
    edf, dd = encode(df)
    dd.original_to_encoded("column1", "valueA")
    #  >>  1
    dd.encoded_to_original("column1", 1)
    #  >> "valueA"
    __________________________________________________
    """

    def __init__(self, dataframe):
        """
        -------------------------------------------------
        :param output_default_dict: the default dictionary generated by this encoder
        __________________________________________________
        """
        def_dict = defaultdict(LabelEncoder)
        clean_dataframe = dataframe.apply(clean_nulls)
        clean_dataframe.apply(lambda x: def_dict[x.name].fit_transform(x))
        def_dict["__columns__"].fit_transform(clean_dataframe.columns)
        self.set_column_encoders(clean_dataframe.columns)
        self._def_dict = def_dict

    def __repr__(self):
        return "DDTranslator for values of: " + str(list(self._def_dict.keys()))

    @staticmethod
    def _enumerate_letters(count):
        """
        Generates a list of unique capital letter strings accordingly
        eg. ['A', 'B', ... , 'AA', 'BB', 'CC', ...]

        :param df: number of unique letter strings to return
        :returns: list <str>: list of capital letter strings
        """

        letters_in_alphabet = 26

        class _unique_list(list):
            """
            _unique_list extends the standard list for this application
            and will only allow items not already in the list to be appended
            NOTE: this is *only* for this application, as this implementation
            will break if items are removed

            Adds a method, 'contains' which will check the internal set of already
            seen items and prevent appending to the list in the case it is already there
            """

            def __init__(self):
                self._seen = set()

            def append(self, item):
                if item not in self._seen:
                    self._seen.add(item)
                    super().append(item)  # append the item to the list

            def contains(self, item):
                return item in self._seen

        results = _unique_list()

        for i in range(count):
            column_title = string.ascii_uppercase[i % letters_in_alphabet]
            # must loop here in the instance that the column_title is in the set already
            while True:
                if results.contains(column_title):
                    column_title += string.ascii_uppercase[i % letters_in_alphabet]
                else:
                    break
            results.append(column_title)
        return results

    def set_column_encoders(self, columns):
        codes = self._enumerate_letters(columns.size)
        self._column_encoder = dict(enumerate(codes))
        self._column_decoder = {code: idx for idx, code in enumerate(codes)}

    def original_to_encoded(self, column_label, orig_value):
        """
        -------------------------------------------------
        :param column_label: the column name for the lookup
        :param orig_value: the original values
        :return: returns the encoded value mapped to that original value,
        for this column_label
        :raises: dd.original_to_encoded("wrong_column_name", 1) =>
             sklearn.exceptions.NotFittedError
        :raises: dd.original_to_encoded("petallengthincm", "999") =>
             ValueError if no 999 in original data set
        __________________________________________________
        """
        clean_orig_value = clean_nulls(orig_value)
        encoded = self._def_dict[column_label].transform(clean_orig_value)

        if orig_value.var_type == "discrete":
            encoded = encoded.astype(str)

        encoded_col_label = self._def_dict["__columns__"].transform([column_label])[0]
        encoded_col_label = self._column_encoder[encoded_col_label]

        return encoded, encoded_col_label

    def encoded_to_original(self, column_label, encoded_value):
        """
        -------------------------------------------------
        :param column_label: the column name for the lookup
        :param encoded_value: the encoded values to get originals
        :return: returns the original value mapped to that encoded value,
        for this column_label
        :raises: dd.encoded_to_original("wrong_column_name", 1) =>
            sklearn.exceptions.NotFittedError
        :raises: dd.encoded_to_original("petallengthincm", "999") =>
            ValueError if no 999 in encoded data set
        __________________________________________________
        """
        decoded_col_label = self._def_dict["__columns__"].inverse_transform(
            [column_label]
        )[0]
        decoded = self._def_dict[decoded_col_label].inverse_transform(
            encoded_value.astype(np.int)
        )

        return MondoSeries(decoded, name=decoded_col_label)

    def column_has_null_values(self, column):
        """
        -------------------------------------------------
        :param column_label: the column name for the lookup
        :return: returns True if variable is has null values, and False if it does not
        :raises: dd.variable_is_continuous("alskdjalskjdaldj") =>
            KeyError if no variable named 'alskdjalskjdaldj' in data set
        __________________________________________________
        """
        return column.isnull().any()

    def variable_is_continuous(self, column_label):
        """
        -------------------------------------------------
        :param column_label: the column name for the lookup
        :return: returns True if variable is continuous, and False if it is not
        :raises: dd.variable_is_continuous("alskdjalskjdaldj") =>
            KeyError if no variable named 'alskdjalskjdaldj' in data set
        __________________________________________________
        """
        return self._column_label_is_continuous[column_label]
