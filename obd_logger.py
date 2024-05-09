from influx_connection import InfluxConnection
from obd_connection import ObdConnection
from dotenv import load_dotenv
import os

load_dotenv()

make = os.getenv("MAKE")
model = os.getenv("MODEL")
plate = os.getenv("PLATE")

influx = InfluxConnection(make, model, plate)


def callback(field_name, value):
    influx.write_point(field_name, value)


obd = ObdConnection("/dev/ttys008", callback)

while True:
    pass
