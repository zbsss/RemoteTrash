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
                    "keyyy": "valll"
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
        "id": "dev1",
        "long": "45.555",
        "lat": "333.444"
    }
]
# register(devs_data)
get_dev("dev2")