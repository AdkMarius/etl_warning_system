from flask import (
    Blueprint, flash, g, request, url_for, jsonify
)
from werkzeug.exceptions import abort

import requests
import logging
from datetime import datetime
from requests.auth import HTTPBasicAuth

from warning_system import config
from warning_system.models import datas, ids
from warning_system.custom import error, utils

bp = Blueprint('newIndicator', __name__, url_prefix='/api')
filename = "static/dataorg.csv"


s = requests.Session()
s.auth = HTTPBasicAuth(username="admin", password="district")


@bp.route("/dataElements", methods=['GET'])
def get_data_elements():
    try:
        if request.args.get('filter') is not None:
            filter_string = request.args.get('filter')
            api_url = config.api_url + f"/dataElements?filter=displayName:ilike:{filter_string}"
            result = datas.fetch_from_dhis2(api_url)
            return jsonify(result)
        else:
            page = int(request.args.get("page", 1))
            api_url = config.api_url + f"/dataElements?page={page}"
            result = datas.fetch_from_dhis2(api_url)
            return jsonify(result)
    except error.APIError as e:
        logging.error(f"APIError: {e}")


@bp.route("/diseases", methods=['GET'])
def get_diseases():
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
    else:
        response["dataElements"] = data_formatted

    response["pager"] = pager

    return jsonify(response)


@bp.route('/create-new-indicator', methods=['POST'])
def create_new_indicator():
    req_data = request.get_json()

    # fetch the dataSets related to the selected dataElements
    api_url = config.api_url + f"/dataSets?filter=dataSetElements.dataElement.id:eq:{req_data['dataElement']['id']}"
    result = datas.fetch_from_dhis2(api_url)
    if len(result['dataSets']) >= 1:
        data_set = result['dataSets'][0]
    else:
        return jsonify({
            'httpStatus': 'Not Found',
            'httpStatusCode': 404,
            'message': 'Dataset is not found for this dataElement!'
        })

    # get the periodType of the dataSets
    api_url = config.api_url + f'/dataSets/{data_set["id"]}'
    result = datas.fetch_from_dhis2(api_url)
    period_type = result['periodType']

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
        return jsonify({
            'httpStatus': 'Successfully',
            'httpStatusCode': 200,
            'message': 'Data scheduled with success!'
        })
    except Exception as e:
        return jsonify({
            'httpStatus': 'Failed',
            'httpStatusCode': 500,
            'message': 'Error occurs. Please try again later!'
        })
