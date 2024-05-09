import os
from dotenv import load_dotenv
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

load_dotenv()


class InfluxConnection:
    def __init__(self, make, model, plate):
        self.url = os.getenv("INFLUX_URL")
        self.org = os.getenv("INFLUX_ORG")
        self.bucket = os.getenv("INFLUX_BUCKET")
        self.token = os.getenv("INFLUX_TOKEN")
        logger.debug("Url: %s" % self.url)
        logger.debug("Org: %s" % self.org)
        logger.debug("Bucket: %s" % self.bucket)
        logger.debug("Token: %d characters (hidden)" % len(self.token))

        self.make = make
        self.model = model
        self.plate = plate

        self.client = influxdb_client.InfluxDBClient(
            url=self.url, org=self.org, token=self.token
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        logger.info("Influx connection created")

    def write_point(self, field_name, value):
        p = (
            influxdb_client.Point("obd-data")
            .tag("make", self.make)
            .tag("model", self.model)
            .tag("plate", self.plate)
            .field(field_name, value)
        )

        try:
            self.write_api.write(bucket=self.bucket, org=self.org, record=p)
        except:
            logger.exception("Exception during writing point")
