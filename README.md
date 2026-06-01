# Datasette on Docker

## Start

```bash
docker network create webnet   # once
docker compose run --rm datasette-inspect   # after adding or changing .db files in data/
docker compose up -d --build
```

Put SQLite files in `data/`. For GitHub auth: `cp .env.example .env` and fill in the values.

Datasette listens on port **8001** on the `webnet` network—point your reverse proxy at `datasette:8001`.

## Upgrade Datasette

Change the version in `Dockerfile`, then:

```bash
docker compose down
docker compose build
docker compose up -d
```
