from urllib.parse import urlparse

import validators


def is_url(url, strict=False):

    final_url = _get_final_url(url, strict)

    is_url_result = _is_url_by_validators(final_url)

    return is_url_result


def _is_url_by_validators(url):

    result = validators.url(url)
    return bool(result)


def _is_url_by_urlparse(url):

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def _get_final_url(url, strict):

    if not strict:
        if "http" not in url:
            final_url = "https://" + url
        else:
            final_url = url

    elif strict:
        final_url = url

    else:
        raise NotImplementedError

    return final_url
