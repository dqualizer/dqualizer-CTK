import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "PpJnMqWR0RkZGbd6GxocbTs9VyiHjFnOKpCiTVRaPYc3qySPKgS8oevYQwq0DNnnX7NZRlzcaAZ6bfcU5f1cuw==" # os.environ.get("INFLUXDB_TOKEN")
org = "Dqualizer"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket = "ResilienceTesting"

write_api = write_client.write_api(write_options=SYNCHRONOUS)
query_api = write_client.query_api()


def write_monitoring_data(measurement_id, tag_name, tag_value, field, value):
    point = (
        Point(measurement_id)
        .tag(tag_name, tag_value)
        .field(field, value)
    )
    write_api.write(bucket=bucket, org="Dqualizer", record=point)