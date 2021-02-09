# zeby zadzialalo trzeba wyexportowac zmienna srodowiskowa z sciezka do pliku z credentialami 
# najlepiej chyba uzyc bezwzglednej sciezki
# np. export GOOGLE_APPLICATION_CREDENTIALS=""

import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage

# Explicitly create a credentials object. This allows you to use the same
# credentials for both the BigQuery and BigQuery Storage clients, avoiding
# unnecessary API calls to fetch duplicate authentication tokens.
credentials, your_project_id = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Make clients.
bqclient = bigquery.Client(credentials=credentials, project=your_project_id,)
bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)

# Download query results.
query_string = """
SELECT * from `tirprojekt.set_telemetry.records_error_records` order by timestamp desc 
"""

dataframe = (
    bqclient.query(query_string)
    .result()
    .to_dataframe(bqstorage_client=bqstorageclient)
)
print(dataframe.head())