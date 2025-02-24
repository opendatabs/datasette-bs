FROM datasetteproject/datasette:0.64.6

RUN apt-get update && \
    apt-get install -y \
      spatialite-bin \
      libsqlite3-mod-spatialite && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install datasette-leaflet-geojson
