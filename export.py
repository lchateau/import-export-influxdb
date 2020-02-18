from influxdb import InfluxDBClient

CONFIG_FILE_NAME = "config.env"

with open(CONFIG_FILE_NAME, "r") as config_file:
    args = config_file.readline().split(":")
    influx_username = args[0]
    influx_password = args[1]

client = InfluxDBClient(host="localhost", port=8086,
                        username=influx_username, password=influx_password)

print(client.get_list_database())