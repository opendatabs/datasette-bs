# How to upgrade to a more recent Datasette Version
Change the version number in Dockerfile, and run the following sequence of commands in the root directory.

$docker compose down

$docker compose build

$docker compose up -d

You can add additional steps in the Dockerfile, e.g. to install Datasette plugins
