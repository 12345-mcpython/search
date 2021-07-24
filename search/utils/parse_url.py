from posixpath import normpath
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse
import re


def url_join(base, url):
    if not re.match("[a-zA-z]+://[^\s]*", url):
        url1 = urljoin(base, url)
        arr = urlparse(url1)
        path = normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))
    else:
        return url


def get_url_scheme(url):
    return urlparse(url)[0] + "://" + urlparse(url)[1]
