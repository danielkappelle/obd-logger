import obd
from influx_connection import InfluxConnection
from dotenv import load_dotenv
import os
load_dotenv()

make = os.getenv('MAKE')
model = os.getenv('MODEL')
plate = os.getenv('PLATE')

influx = InfluxConnection(make, model, plate)
print(influx)

def on_rpm(r):
  influx.write_point("rpm", r.value.magnitude)
  print(r.value)

connection = obd.Async(portstr='/dev/ttys005', baudrate=115200)
connection.watch(obd.commands.RPM, callback=on_rpm)
connection.start()

while(True):
  pass