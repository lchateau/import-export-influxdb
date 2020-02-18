from influxdb import InfluxDBClient

CONFIG_FILE_NAME = "config.env"
db_name = "test"

with open(CONFIG_FILE_NAME, "r") as config_file:
    args = config_file.readline().split(":")
    influx_username = args[0]
    influx_password = args[1]

client = InfluxDBClient(host="localhost", port=8086,
                        username=influx_username, password=influx_password)

# print(client.get_list_database())
client.switch_database(db_name)

start_date = "'2019-01-01'"
end_date = "'2020-03-01'"

request = "SELECT * FROM test_temperature WHERE time >= " + \
    start_date + " AND time <= " + end_date

result = client.query(request)
column_names = result.raw["series"][0]["columns"]
csv_header = ""

for column in column_names:
    csv_header += column + ","

csv_header = csv_header[:-1]
print(csv_header)
pt = result.get_points()

for r in pt:
    line = ""
    for column in column_names:
        line += str(r[column]) + ","
    line = line[:-1]
    print(line)
