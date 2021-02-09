# project_id = 'YOUR_PROJECT_ID'
# cloud_region = 'us-central1'
# registry_id = 'your-registry-id'
# device_id = 'your-device-id'
# certificate_file = 'path/to/certificate.pem'
from google.api_core.exceptions import AlreadyExists
from google.cloud import iot_v1
from google.cloud import pubsub
import os
import io
from google.protobuf import field_mask_pb2 as gp_field_mask

CONFIGURATION = {
    "project_id" : "tirprojekt",
    "cloud_region" : "europe-west1",
    "registry_id" : "smartbins",
    "private_key_file" : "rsa_private",
    "algorithm" : "RS256",
    "ca_certs" : "roots.pem",
    "mqtt_bridge_hostname" : "mqtt.googleapis.com",
    "mqtt_bridge_port" : 8883,


}

def register(dev_data_list):
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(CONFIGURATION["project_id"], CONFIGURATION["cloud_region"], CONFIGURATION["registry_id"])

    

    # Note: You can have multiple credentials associated with a device.
    devs_to_ret = []
    for dev in dev_data_list:
        key_file_private = "rsa_private_{deviceid}.pem".format(deviceid=dev['id'])
        cert_file = "rsa_cert_{deviceid}.pem".format(deviceid=dev['id'])
        os.system('openssl req -x509 -newkey rsa:2048 -keyout {key_file} -nodes -out {cert_file} -subj "/CN=unused"'.format(key_file=key_file_private, cert_file=cert_file))

        with io.open(cert_file) as f:
            certificate = f.read()

            device_template = {
                "id": dev['id'],
                "credentials": [
                    {
                        "public_key": {
                            "format": iot_v1.PublicKeyFormat.RSA_X509_PEM,
                            "key": certificate,
                        }
                    }
                ],
                "metadata": {
                    "long": dev['long'],
                    "lat": dev['lat']
                }
            }
        devs_to_ret.append(client.create_device(request={"parent": parent, "device": device_template}))
    return devs_to_ret


def get_dev(devid):
    print("Getting device")
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(CONFIGURATION["project_id"], CONFIGURATION["cloud_region"], CONFIGURATION["registry_id"], devid)
    field_mask = gp_field_mask.FieldMask(
        paths=[
            "id",
            "name",
            "num_id",
            "credentials",
            "last_heartbeat_time",
            "last_event_time",
            "last_state_time",
            "last_config_ack_time",
            "last_config_send_time",
            "blocked",
            "last_error_time",
            "last_error_status",
            "config",
            "state",
            "log_level",
            "metadata",
            "gateway_config",
        ]
    )
    device = client.get_device(request={"name": device_path, "field_mask": field_mask})

    # print("Id : {}".format(device.id))
    # print("Name : {}".format(device.name))
    # print("Metadata: {}".format(device.metadata))
    # print("\tdata: {}".format(device.config.binary_data))
    # print("\tversion: {}".format(device.config.version))
    # print("\tcloudUpdateTime: {}".format(device.config.cloud_update_time))

    return device













devs_data = [
    {
        "id": "smart-bin-1",
        "lat": "50.059215167684435",
        "long": "19.938240760722554"
    },
    {
        "id": "smart-bin-2",
        "lat": "50.059779969290204", 
        "long": "19.94242500699472"
    },
    {
        "id": "smart-bin-3",
        "lat": "50.06629501635049", 
        "long": "19.939762027346998"
    },
    {
        "id": "smart-bin-4",
        "lat": "50.06519306679963", 
        "long": "19.951080949060767"
    },
    {
        "id": "smart-bin-5",
        "lat": "50.068464283479756", 
        "long": "19.952679545724695"
    },
    {
        "id": "smart-bin-6",
        "lat": "50.0676485127072", 
        "long": "19.91723601190027"
    },
    {
        "id": "smart-bin-7",
        "lat": "50.069948600070326", 
        "long": "19.90546647887831"
    },
    {
        "id": "smart-bin-8",
        "lat": "50.06298441031591",
        "long": "19.90339602647755"
    },
    {
        "id": "smart-bin-9",
        "lat": "50.06965087655583", 
        "long": "19.925862209204546"
    },
    {
        "id": "smart-bin-10",
        "long": "50.05888454902623",
        "lat": "19.93300508892388"
    },
]
register(devs_data)
# get_dev("dev2")