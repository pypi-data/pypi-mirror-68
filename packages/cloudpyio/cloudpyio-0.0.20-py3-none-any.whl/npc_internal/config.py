import os


# SERVER_URL = os.environ.get('SERVER_URL', 'http://numpy-cloud-api.herokuapp.com/')
SERVER_URL = os.environ.get('SERVER_URL', 'http://localhost:9090/')
DATA_BUCKET = os.environ.get('DATA_BUCKET', 'cloudpy-data')
MAX_MEMORY = int(os.environ.get('MAX_MEMORY', 128 * 1e6))
MAX_LIBRARY_MEMORY = int(os.environ.get('MAX_LIBRARY_MEMORY', 1e9))
