from flask import (
    Blueprint, request, jsonify
)
import requests
from requests.auth import HTTPBasicAuth

import logging
from datetime import datetime

from warning_system import config
from warning_system.models import datas
from warning_system.custom import error

bp = Blueprint('newIndicator', __name__, url_prefix='/api')
filename = "static/dataorg.csv"


s = requests.Session()
s.auth = HTTPBasicAuth(username="admin", password="district")


@bp.route("/dataElements", methods=['GET'])
def get_data_elements():
    # provide all data elements in dhis2
    try:
        if request.args.get('filter') is not None:
            filter_string = request.args.get('filter')
            api_url = config.api_url + f"/dataElements?filter=displayName:ilike:{filter_string}"
            result = datas.fetch_from_dhis2(api_url)
            logging.info("filtered dataElements fetched successfully")
            return jsonify(result)
        else:
            page = int(request.args.get("page", 1))
            api_url = config.api_url + f"/dataElements?page={page}"
            result = datas.fetch_from_dhis2(api_url)
            logging.info("dataElements fetched successfully")
            return jsonify(result)
    except error.APIError as e:
        logging.error(f"APIError: {e}")


@bp.route("/diseases", methods=['GET'])
def get_diseases():
    # provide all infectious and notifiable diseases with pagination

    # Get pagination parameters from the request
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 25))
    offset = (page - 1) * limit

    total_diseases, paginated_diseases_dict = 0, []
    if request.args.get('filter') is None:
        total_diseases, diseases = datas.fetch_notifiable_and_infectious_diseases()
        paginated_diseases = diseases[offset:offset + limit]

        paginated_diseases_dict = [
            {
                "id": f"{paginated_disease.id}",
                "code": paginated_disease.code,
                "displayName": paginated_disease.name
            }
            for paginated_disease in paginated_diseases
        ]
        logging.info("disease list fetched successfully")
    elif request.args.get('filter') is not None:
        filter_value = request.args.get('filter')
        filter_type = request.args.get('filterType')

        total_diseases, diseases = datas.fetch_filtered_notifiable_and_infectious_diseases(filter_type, filter_value)
        paginated_diseases = diseases[offset:offset + limit]

        paginated_diseases_dict = [
            {
                "id": f"{paginated_disease.id}",
                "code": paginated_disease.code,
                "displayName": paginated_disease.name
            }
            for paginated_disease in paginated_diseases
        ]
        logging.info("filtered disease list fetched successfully")

    # Create the response with pagination info
    response = {
        "dataElements": paginated_diseases_dict,
        "pager": {
            "nextPage": f"http://127.0.0.1:5000/api/diseases?page={page + 1}&limit=25",
            "page": page,
            "pageCount": (total_diseases + limit - 1) // limit,
            "pageSize": limit,
            "total": total_diseases
        }
    }

    return jsonify(response)


@bp.route("/indicators", methods=['GET'])
def get_indicators():
    # provide all information about the indicators

    page_size = 25
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * page_size

    data = []
    filtered_indicators = []

    unique_indicators = datas.fetch_data_indicators()
    data_formatted = [
        {
            "id": f"{index}",
            "displayName": indicator
        } for index, indicator in enumerate(unique_indicators)
    ]

    if request.args.get('filter') is not None:
        filter_str = request.args.get('filter')
        filtered_indicators = [elt for elt in data_formatted if filter_str.lower() in elt["displayName"].lower()]

    if page > 1:
        if len(filtered_indicators) > 1:
            data = filtered_indicators[offset:offset + page_size]
        else:
            data = data_formatted[offset:offset + page_size]

    total = len(unique_indicators)
    page_count = (total + page_size - 1) // page_size

    pager = {
            "nextPage": f"http://127.0.0.1:5000/api/indicators?page={page + 1}",
            "page": page,
            "pageCount": page_count,
            "pageSize": page_size,
            "total": total
    }

    response = {}
    if len(data) > 0:
        response["dataElements"] = data
    elif request.args.get('filter') is not None:
        response["dataElements"] = filtered_indicators
        logging.info("filtered indicators fetched with success")
    else:
        response["dataElements"] = data_formatted
        logging.info("indicators fetched with success")

    response["pager"] = pager

    return jsonify(response)


@bp.route('/create-new-indicator', methods=['POST'])
def create_new_indicator():
    # save the new indicator created by the user in the indicator.csv

    req_data = request.get_json()

    # set the two data sets for weekly and daily data
    data_sets = [
        {
            "displayName": "IDS daily - Report: Suspected, Confirm, Death, Recovered",
            "id": "rTPYTgYoxAQ"
        },
        {
            "displayName": "IDS - Report: Suspected, Confirm, Death",
            "id": "ZyZmZTUwctj"
        }
    ]

    # define the periodType and the dataSets according to the period
    if 'daily' in req_data['indicator']['displayName'].lower():
        data_set = data_sets[0]
        period_type = "Daily"
    else:
        data_set = data_sets[1]
        period_type = "Weekly"

    indicator_data = {
        "diseaseId": req_data['disease']['id'],
        "diseaseCode": req_data['disease']['code'],
        "diseaseDisplayName": req_data['disease']['displayName'],
        "indicatorDisplayName": req_data['indicator']['displayName'],
        "dataElementId": req_data['dataElement']['id'],
        "dataElementDisplayName": req_data['dataElement']['displayName'],
        "dataSetId": data_set["id"],
        "dataSetPeriod": period_type,
        "createdDate": datetime.now()
    }

    try:
        datas.store_data_indicator(indicator_data)
        logging.info("new indicator created successfully at {}".format(datetime.now()))
        return jsonify({
            'httpStatus': 'Successfully',
            'httpStatusCode': 200,
            'message': 'Data scheduled with success!'
        })
    except Exception as e:
        logging.error(f"error server while creating new indicator: {e}")
        return jsonify({
            'httpStatus': 'Failed',
            'httpStatusCode': 500,
            'message': 'Error occurs. Please try again later!'
        })
