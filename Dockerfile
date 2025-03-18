FROM datasetteproject/datasette:0.64.6

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
      spatialite-bin \
      libsqlite3-mod-spatialite && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Datasette plugins
RUN pip install --user --no-cache-dir datasette-leaflet-geojson==0.8.2
RUN pip install --user --no-cache-dir datasette-cluster-map==0.18.2
RUN pip install --user --no-cache-dir datasette-vega==0.6.2
RUN pip install --user --no-cache-dir datasette-marimo==0.1.3