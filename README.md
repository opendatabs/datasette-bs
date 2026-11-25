# Datasette Basel-Stadt

Source for the Datasette instance (plugins, templates, static assets, `data/metadata.yml`).
A GitHub Actions workflow ([.github/workflows/docker.yml](.github/workflows/docker.yml)) builds the image and pushes it to
`ghcr.io/opendatabs/datasette-bs` (`latest` on the default branch, plus `sha-…` and tag versions).

The image contains everything except the data: put `*.db` files and the generated `counts.json` in `/mnt/data`.
Running the container (docker compose, CI) lives in the internal GitLab deploy project.

Python dependencies are managed with [uv](https://docs.astral.sh/uv/) (`pyproject.toml` + `uv.lock`).

## Local development

```bash
uv sync
cp .env.example .env   # GitHub auth values
uv run datasette inspect data/*.db --inspect-file=data/counts.json --load-extension=spatialite
uv run datasette serve -i data/*.db --inspect-file=data/counts.json --metadata data/metadata.yml \
  --template-dir=templates --plugins-dir=plugins --static bs:static/bs --load-extension=spatialite
```

SpatiaLite must be installed locally (`brew install spatialite-tools`).

## Dependencies

Add or upgrade a plugin with `uv add <package>==<version>` (or `uv lock --upgrade-package <package>`), commit `pyproject.toml` and `uv.lock`, and merge to `main`; the workflow publishes a new image. Renovate opens PRs for version bumps.
