FROM datasetteproject/datasette:0.65.1

# Install Datasette plugins
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
