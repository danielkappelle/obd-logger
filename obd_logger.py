from influx_connection import InfluxConnection
from obd_connection import ObdConnection
from dotenv import load_dotenv
import logging
import os
import threading

file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_formatter = logging.Formatter("[%(name)s] %(message)s")
root_logger = logging.getLogger()

file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(file_formatter)
root_logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)
root_logger.addHandler(console_handler)

root_logger.setLevel(logging.DEBUG)


logger = logging.getLogger(__name__)
logger.info("OBD Logger started")

load_dotenv()

make = os.getenv("MAKE")
model = os.getenv("MODEL")
plate = os.getenv("PLATE")

influx = InfluxConnection(make, model, plate)


def callback(field_name, value):
    influx.write_point(field_name, value)


obd = ObdConnection("/dev/ttys008", callback)

progress_chars = ["|", "/", "-", "\\"]
progress_i = 0


def print_progress():
    global progress_chars, progress_i
    print("\r" + progress_chars[progress_i], end="", flush=True)
    progress_i = (progress_i + 1) % len(progress_chars)
    threading.Timer(1.0, print_progress).start()


print_progress()

while True:
    pass
