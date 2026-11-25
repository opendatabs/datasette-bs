FROM python:3.15-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /usr/local/bin/uv

RUN apt-get update \
    && apt-get install -y --no-install-recommends libsqlite3-mod-spatialite \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY templates /app/templates
COPY static /app/static
COPY plugins /app/plugins
COPY data/metadata.yml /app/metadata.yml

EXPOSE 8001

CMD ["/bin/sh", "-c", "datasette serve -i /mnt/data/*.db --inspect-file=/mnt/data/counts.json --metadata /app/metadata.yml --host 0.0.0.0 --port 8001 --setting max_returned_rows 10000 --setting default_page_size 20 --setting sql_time_limit_ms 50000 --setting facet_time_limit_ms 50000 --setting max_csv_mb 0 --setting force_https_urls 1 --load-extension=spatialite --template-dir=/app/templates --plugins-dir=/app/plugins --static bs:/app/static/bs"]
