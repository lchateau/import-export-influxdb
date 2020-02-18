from influxdb import InfluxDBClient

CONFIG_FILE_NAME = "config.env"
db_name = "test"
measurement = "test_temperature"

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


def export(start_date, end_date, measurement):
    request = "SELECT * FROM " + measurement + " WHERE time >= " + \
    start_date + " AND time <= " + end_date

    result = client.query(request)
    column_names = result.raw["series"][0]["columns"]
    csv_header = ""

    for column in column_names:
        csv_header += column + ","

    csv_header = csv_header[:-1]
    
    points = pt = result.get_points()

    with open("export.csv", "w") as export_file:
        export_file.write(csv_header + "\n")
        for point in points:
            line = ""
            for column in column_names:
                line += str(point[column]) + ","
            line = line[:-1]
            export_file.write(line + "\n")


export(start_date, end_date, measurement)

# json_body = [
#     {
#         "measurement": "test_temperature",
#         "time": "2020-02-14T18:22:06.232589412Z",
#         "fields": {
#             "lon": 7.22
#         }
#     }
# ]

# # client.write_points(json_body)
