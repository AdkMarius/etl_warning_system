import csv
import logging
import os
import threading
import time
import functools
from dotenv import load_dotenv

import schedule

from warning_system.models import ids, datas
from warning_system.custom import utils, error
import warning_system.config as config

load_dotenv()  # Load environment variables once at the start

filename = os.getcwd() + '/static/indicator.csv'

# get the organisation unit id from .env
ORG_UNIT_ID = os.environ.get('GNUHEALTH_ORG_UNIT_ID')


def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                logging.error(f"Exception while sending data: {traceback.format_exc()}")
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator


def extract_info(period_type: str) -> list:
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header_row = next(reader)

        for row in reader:
            if row[7].lower() == period_type.lower():
                info = {
                    'diseaseCode': row[1],
                    'indicatorName': row[3],
                    'dataElementId': row[4],
                    'dataSetId': row[6],
                    'period': row[7]
                }
                data.append(info)

    return data


# send data to dhis2 server
def send_data(data: dict):
    try:
        # send the new indicator created
        api_url = config.api_url + f'/dataValueSets'
        r = datas.send_new_indicator(data, api_url)
    except error.APIError as e:
        logging.error(f"{e}")


# send weekly all new indicator
@catch_exceptions(cancel_on_failure=True)
def send_weekly_data():
    weekly_data = extract_info("weekly")
    for index, data in enumerate(weekly_data):
        logging.info(f"data process for the {index} weekly data")
        value = ids.calculate_new_indicator(data['indicatorName'].upper(), data['diseaseCode'])
        current_date, period = utils.weekly_period()
        payload = {
            "dataSet": data['dataSetId'],
            "completeDate": current_date.strftime("%Y-%m-%d"),
            "orgUnit": ORG_UNIT_ID,
            "period": period,
            "dataValues": [
                {
                    "dataElement": data['dataElementId'],
                    "value": value
                }
            ]
        }
        # send_data(payload)
        print(payload)
    logging.info("all weekly data sent successfully")


# send all daily new indicator
@catch_exceptions(cancel_on_failure=True)
def send_daily_data():
    daily_data = extract_info("daily")
    for index, data in enumerate(daily_data):
        logging.info(f"data process for the {index} daily data")
        value = ids.calculate_new_indicator(data['indicatorName'].upper(), data['diseaseCode'])
        previous_date, period = utils.date_and_period()
        payload = {
            "dataSet": data['dataSetId'],
            "completeDate": previous_date.strftime("%Y-%m-%d"),
            "orgUnit": ORG_UNIT_ID,
            "period": period,
            "dataValues": [
                {
                    "dataElement": data['dataElementId'],
                    "value": value
                }
            ]
        }
        # send_data(payload)
        print(payload)
    logging.info("all daily data sent successfully")


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def job_scheduler():
    # send data frequently
    schedule.every().day.at("00:00").do(run_threaded, send_weekly_data)
    schedule.every().monday.at("00:00").do(run_threaded, send_daily_data)

    # for testing
    # schedule.every(2).minutes.do(run_threaded, send_weekly_data)
    # schedule.every(2).minutes.do(run_threaded, send_daily_data)

