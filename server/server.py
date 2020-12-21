import psycopg2
import json
from paho.mqtt.client import Client
from config import configDB, configMQTT
from datetime import datetime

# read database configuration

paramsDB = configDB()
# connect to the PostgreSQL database
paramsMQTT = configMQTT()
conn = psycopg2.connect(**paramsDB)

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    payload = str(message.payload.decode("utf-8"))
    payload_dict = json.loads(payload)
    device_id = message.topic.split('/')[-1]

    print(device_id)
    insert_record(conn, device_id, float(payload_dict['capacity']), float(payload_dict['battery']), datetime.now().isoformat(timespec='seconds'))

def insert_record(conn, device_id, capacity, battery, time):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO records(device_id, capacity, battery, time)
             VALUES(%s, %s, %s, %s) RETURNING id;"""
    vendor_id = None
    try:

        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (device_id, capacity, battery, time))
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            pass

    return vendor_id

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = [
    """
        DROP TABLE records
    """,
    """
        CREATE TABLE records (
             id SERIAL PRIMARY KEY,
             device_id INTEGER,
             capacity REAL,
             battery REAL,
             time TIMESTAMP
         )
    """
    ]
    # commands = (
    #     """
    #     CREATE TABLE records (
    #         id INTEGER PRIMARY KEY,
    #         device_id INTEGER,
    #         capacity REAL,
    #         battery REAL
    #         time TIMESTAMP
    #     )
    #     CREATE TABLE vendors (
    #         vendor_id SERIAL PRIMARY KEY,
    #         vendor_name VARCHAR(255) NOT NULL
    #     )
    #     """,
    #     """ CREATE TABLE parts (
    #             part_id SERIAL PRIMARY KEY,
    #             part_name VARCHAR(255) NOT NULL
    #             )
    #     """,
    #     """
    #     CREATE TABLE part_drawings (
    #             part_id INTEGER PRIMARY KEY,
    #             file_extension VARCHAR(5) NOT NULL,
    #             drawing_data BYTEA NOT NULL,
    #             FOREIGN KEY (part_id)
    #             REFERENCES parts (part_id)
    #             ON UPDATE CASCADE ON DELETE CASCADE
    #     )
    #     """,
    #     """
    #     CREATE TABLE vendor_parts (
    #             vendor_id INTEGER NOT NULL,
    #             part_id INTEGER NOT NULL,
    #             PRIMARY KEY (vendor_id , part_id),
    #             FOREIGN KEY (vendor_id)
    #                 REFERENCES vendors (vendor_id)
    #                 ON UPDATE CASCADE ON DELETE CASCADE,
    #             FOREIGN KEY (part_id)
    #                 REFERENCES parts (part_id)
    #                 ON UPDATE CASCADE ON DELETE CASCADE
    #     )
    #     """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    # create_tables()
    # BROKER = ("34.70.234.204", 1883, 60)  # host, port, keepalive
    BROKER = (paramsMQTT['host'], int(paramsMQTT['port']), int(paramsMQTT['keepalive']))  # host, port, keepalive
    MAIN_TOPIC = paramsMQTT['main_topic']
    client = Client("srv")
    #insert_record(1, 72.44, 21.01, '2020-12-21T12:01:22')

    client.connect(*BROKER)
    client.subscribe(MAIN_TOPIC + "/+")
    client.on_message = on_message
    client.loop_forever()
    conn.close()
