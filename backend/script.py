import csv
import re
from datetime import datetime

from warning_system.models import ids, datas
from warning_system.custom import utils, error
import warning_system.config as config

filename = 'static/indicator.csv'

if __name__ == '__main__':
    data = []
    with open(filename, newline='') as csvfile:
        delimiters = r"[-: .]+"
        reader = csv.DictReader(csvfile)
        for row in reader:
            createdDateStr = re.split(delimiters, row['createdDate'])
            createdDate = datetime(int(createdDateStr[0]), int(createdDateStr[1]), int(createdDateStr[2]))
            if createdDate.date() == datetime.now().date():
                data.append(row)

    for row in data:
        # calculate the data Element value
        new_indicator_value = ids.calculate_new_indicator(row['indicatorDisplayName'].upper(), row['diseaseCode'])
        period_type = row['dataSetPeriod']
        if period_type.lower() == 'weekly':
            date, period = utils.weekly_period()
        else:
            date, period = utils.date_and_period()

        payload = {
            "dataSet": f"{row['dataSetId']}",
            "completeDate": date.strftime("%Y-%m-%d"),
            "orgUnit": "ib4dMYZzKNU",
            "period": period,
            "dataValues": [
                {
                    "dataElement": f"{row['dataElementId']}",
                    "value": new_indicator_value
                }
            ]
        }

        print(payload)

        try:
            # send the new indicator created
            api_url = config.api_url + f'/dataValueSets'
            r = datas.send_new_indicator(payload, api_url)
        except error.APIError as e:
            print(f"Error: {e}")
