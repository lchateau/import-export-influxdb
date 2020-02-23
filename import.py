from influxdb import InfluxDBClient
import sys

CONFIG_FILE_NAME = "config.env"
SEPARATOR = "#"

if len(sys.argv) != 4:
    print("Usage : python3 import.py [database] [measurement] [csv_filename]")
    sys.exit(1)

db_name = sys.argv[1]
measurement = sys.argv[2]

with open(CONFIG_FILE_NAME, "r") as config_file:
    args = config_file.readline().splitlines()[0].split(":")
    influx_username = args[0]
    influx_password = args[1]

client = InfluxDBClient(host="localhost", port=8086,
                        username=influx_username, password=influx_password)

client.switch_database(db_name)


def import_csv(filename):
    n_lines, success, fail = 0, 0, 0
    with open(filename, "r") as csv_file:
        columns = csv_file.readline().splitlines()[0].split(SEPARATOR)
        for line in csv_file:
            n_lines += 1
            tab = line.splitlines()[0].split(SEPARATOR)
            json_body = [
                {
                    "measurement": measurement,
                    "time": tab[0],
                    "fields": {
                    }
                }
            ]
            for i, column in enumerate(columns[1:]):
                json_body[0]["fields"].update({column: tab[i+1]})
            if client.write_points(json_body):
                success += 1
            else:
                fail += 1
    print(
        f"Successfully imported {success} measurements from {filename} ({fail} failed of {n_lines})")


import_csv(sys.argv[3])
