# zeby zadzialalo trzeba wyexportowac zmienna srodowiskowa z sciezka do pliku z credentialami 
# najlepiej chyba uzyc bezwzglednej sciezki
# np. export GOOGLE_APPLICATION_CREDENTIALS=""

import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage
import matplotlib.pyplot as plt
from time import sleep
from threading import Thread


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
SELECT * from `tirprojekt.set_telemetry.records` order by timestamp desc 
"""

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 6), constrained_layout=True)
ax1, ax2 = ax


def get_newest_data():
    df = (
        bqclient.query(query_string)
            .result()
            .to_dataframe(bqstorage_client=bqstorageclient)
    )

    # get indices of rows with newest timestamp
    idx = df.groupby(['name'])['timestamp'].transform(max) == df['timestamp']
    newest = df[idx]

    print("NEW DATA LOADED")

    return newest


def update_figure(data):
    ax1.clear()
    _, _, bars = ax1.hist(data['battery'])
    for bar in bars:
        if bar.get_x() <= 25:
            bar.set_facecolor('red')
    ax1.set_title("Battery percentage distribution")
    ax1.set_xlabel("Battery percentage (%)")
    ax1.set_ylabel("Number of devices")
    plt.pause(0.1)

    ax2.clear()
    _, _, bars = ax2.hist(data['fulfillment'])
    for bar in bars:
        if bar.get_x() <= 25:
            bar.set_facecolor('red')
    ax2.set_title("Fulfillment distribution")
    ax2.set_xlabel("Fulfillment percentage (%)")
    ax2.set_ylabel("Number of devices")
    plt.pause(0.1)

    print("PLOT UPDATED")


def update_loop():
    while True:
        newest = get_newest_data()
        update_figure(newest)
        plt.draw()
        sleep(10)


update_thread = Thread(target=update_loop, daemon=True)
update_thread.start()
plt.show()
print("FINISHED!!")
