FROM datasetteproject/datasette:0.65.1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
      spatialite-bin \
      libsqlite3-mod-spatialite && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Datasette plugins
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt