import urllib.parse


def join_url(base_url, url):
    """
    Joins the base_url with the passed url argument

    :rtype: str
    """
    url = urllib.parse.urljoin(base_url, url)

    # Ensure we have a trailing slash (or else mondobrain api complains :/ )
    if not url.endswith("/"):
        url += "/"

    return url
