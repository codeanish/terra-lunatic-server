import requests
import schedule
import time
import logging
from sys import stdout

logger = logging.getLogger()
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler(stdout)
logger.addHandler(consoleHandler)

def sync():
    response = requests.put("http://api:5000/sync")
    logger.info(f"sync() {response.status_code}")

def health_check():
    response = requests.get("http://api:5000/")
    logger.info(f"health_check() {response.status_code}")


if __name__ == "__main__":

    schedule.every(10).seconds.do(health_check)
    schedule.every(1).minute.do(sync)

    while True:
        schedule.run_pending()
        time.sleep(1)