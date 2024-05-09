import os
from dotenv import load_dotenv
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone

load_dotenv()

class InfluxConnection:
  def __init__(self, make, model, plate):
    self.url = os.getenv('INFLUX_URL')
    self.org = os.getenv('INFLUX_ORG')
    self.bucket = os.getenv('INFLUX_BUCKET')
    self.token = os.getenv('INFLUX_TOKEN')

    self.make = make
    self.model = model
    self.plate = plate

    self.client = influxdb_client.InfluxDBClient(url=self.url, org=self.org, token=self.token)
    self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

  def __str__(self):
    s =  "InfluxConnection\n"
    s += "================\n"
    s += "Url: %s\n" % self.url
    s += "Org: %s\n" % self.org
    s += "Token: %s\n" % self.token
    s += "Bucket: %s\n\n" % self.bucket
    s += "Make: %s\n" % self.make
    s += "Model: %s\n" % self.model
    s += "Plate: %s" % self.plate

    return s

  def write_point(self, field_name, value):
    p = influxdb_client.Point("obd-data") \
    .tag("make", self.make) \
    .tag("model", self.model) \
    .tag("plate", self.plate) \
    .field(field_name, value)

    self.write_api.write(bucket=self.bucket, org=self.org, record=p)