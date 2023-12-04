import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "6DPUgkuluiglJehGcOIalA8advCMp7KM6i69o_rtcPloBy9y8XX_Uks8vAdzVAaz9uJmDox96tjOSYSWAdWznw==" # os.environ.get("INFLUXDB_TOKEN")
org = "Dqualizer"
url = "http://localhost:7887"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket = "ResilienceMonitoringData"

write_api = write_client.write_api(write_options=SYNCHRONOUS)
query_api = write_client.query_api()


def write_monitoring_data(measurement_id, tag_name, tag_value, field, value):
    point = (
        Point(measurement_id)
        .tag(tag_name, tag_value)
        .field(field, value)
    )
    write_api.write(bucket=bucket, org="Dqualizer", record=point)