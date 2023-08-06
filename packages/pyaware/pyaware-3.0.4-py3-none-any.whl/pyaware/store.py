import sqlite3
import pyaware
from pyaware.resources import rm
from concurrent.futures import ThreadPoolExecutor
import datetime
import time
import os
import random
import logging

conn = sqlite3.connect(os.path.join(pyaware.config.aware_path, "data.db"), check_same_thread=False)

rm.add_resource(conn, 'db')

rm["db"].execute('''create table if not exists stocks
    (date text, trans text, symbol text,
     qty real, price real)''')
executor = ThreadPoolExecutor(max_workers=10)

print(len(rm["db"].execute("SELECT * from stocks").result().fetchall()))


def write_thing():
    time.sleep(random.random() / 100)
    rm["db"].execute("""insert into stocks
              values (?,?,?,?,?)""", (datetime.datetime.now(), 'BUY', 'RHAT', random.random(), 35.14))
    rm["db"].commit()


logging.basicConfig(level=logging.DEBUG)
while True:
    # TODO Remove or change priority executor as it fails when the timestamp is the same changes

    # time.sleep(0.1)
    executor.submit(write_thing)
    time.sleep(0.01)
