"""Reject requests that combine too many facets.

A distributed scraper walks every combination of ``_facet`` parameters
(each URL = the previous one plus one more facet). Every facet is a full
``GROUP BY`` over the filtered table, so these requests are expensive while
real users rarely combine more than a few facets.

Requests with more than ``max_facets`` facet parameters (``_facet``,
``_facet_array``, ``_facet_date``) get a 400 before any SQL runs.
Facets configured in metadata.yml are not part of the URL and don't count.

Configure in metadata.yml:

    plugins:
      request_guard:
        max_facets: 3
"""

from urllib.parse import parse_qsl

from datasette import hookimpl

FACET_PARAMS = {"_facet", "_facet_array", "_facet_date"}
DEFAULT_MAX_FACETS = 3


def count_facets(query_string: bytes) -> int:
    # parse_qsl also decodes percent-encoded keys such as %5Ffacet
    pairs = parse_qsl(query_string.decode("latin-1"), keep_blank_values=True)
    return sum(1 for key, _ in pairs if key in FACET_PARAMS)


async def reject(send, max_facets: int):
    body = (
        f"Zu viele Facets: Pro Anfrage sind höchstens {max_facets} Facets erlaubt.\n"
        f"Too many facets: at most {max_facets} facets per request.\n"
    ).encode("utf-8")
    await send(
        {
            "type": "http.response.start",
            "status": 400,
            "headers": [
                (b"content-type", b"text/plain; charset=utf-8"),
                (b"content-length", str(len(body)).encode()),
                (b"cache-control", b"no-store"),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body})


@hookimpl
def asgi_wrapper(datasette):
    def wrap(app):
        max_facets = None

        async def guarded(scope, receive, send):
            nonlocal max_facets
            if scope["type"] == "http":
                if max_facets is None:
                    config = datasette.plugin_config("request_guard") or {}
                    max_facets = int(config.get("max_facets", DEFAULT_MAX_FACETS))
                if count_facets(scope.get("query_string", b"")) > max_facets:
                    await reject(send, max_facets)
                    return
            await app(scope, receive, send)

        return guarded

    return wrap
