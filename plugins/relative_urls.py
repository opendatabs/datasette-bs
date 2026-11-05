"""Make Datasette self-links path-relative so pagination keeps the public domain.

With force_https_urls, Datasette builds absolute next/facet URLs from the
incoming Host header. Behind a reverse proxy that Host is often an internal
IP, so "Next page" leaves the public domain and breaks. Path-relative URLs
always stay on whatever host the browser is already using.

Auth callback URLs stay absolute (OAuth providers require a full redirect_uri).
"""

from urllib.parse import urlparse

from datasette import hookimpl

_AUTH_MARKERS = (
    "/-/github-",
    "/-/auth",
    "auth-callback",
    "auth-sign",
)


def _to_relative(url: str) -> str:
    parsed = urlparse(url)
    relative = parsed.path or "/"
    if parsed.query:
        relative += "?" + parsed.query
    if parsed.fragment:
        relative += "#" + parsed.fragment
    return relative


@hookimpl
def startup(datasette):
    original = datasette.absolute_url

    def absolute_url(request, path):
        url = original(request, path)
        if any(marker in url for marker in _AUTH_MARKERS):
            return url
        return _to_relative(url)

    datasette.absolute_url = absolute_url
