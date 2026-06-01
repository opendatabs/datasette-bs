FROM datasetteproject/datasette:0.65.2

# Install Datasette plugins
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
