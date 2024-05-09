# OBD Logger

Use OBD2 serial interface to dump all date in an InfluxDB database.

# Running locally

First make sure `.env` file is set correctly, use `.env.example` as a guide.

1. Spin up InfluxDB, use `$ docker-compose up`
2. Start OBD2 dummy data (see Simulating data below): `$ obdsim`
3. Start the python script `python obd_logger.py`

# Simulating data

In order not to have to be programming from the car, use following project to generate dummy data: https://github.com/oesmith/obdgpslogger
