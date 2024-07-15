import csv
import requests
from requests.auth import HTTPBasicAuth

from proteus import Model

from warning_system import config
from warning_system.custom import error


s = requests.Session()
s.auth = HTTPBasicAuth(username="admin", password="district")


# Confirmed cases
def fetch_confirmed_diseases() -> list:
    config.connect_to_gnu()

    my_model = Model.get('gnuhealth.patient.disease')
    confirmed_diseases = my_model.find([('lab_confirmed', '=', True), ('healed_date', '=', None)])

    return confirmed_diseases


# Suspected cases
def fetch_suspected_diseases() -> list:
    config.connect_to_gnu()

    my_model = Model.get('gnuhealth.patient.disease')
    suspected_diseases = my_model.find([('lab_confirmed', '=', False), ('healed_date', '=', None)])

    return suspected_diseases


# Recovered cases
def fetch_recovered_diseases() -> list:
    config.connect_to_gnu()

    my_model = Model.get('gnuhealth.patient.disease')
    recovered_diseases = my_model.find([('lab_confirmed', '=', True), ('healed_date', '!=', None)])

    return recovered_diseases


# Deaths
def fetch_deaths() -> list:
    config.connect_to_gnu()

    my_model = Model.get('gnuhealth.death_certificate')
    deaths = my_model.find([])

    return deaths


# Occupied Beds : B
def fetch_occupied_bed() -> list:
    config.connect_to_gnu()

    my_model = Model.get('gnuhealth.inpatient.registration')
    occupied_bed = my_model.find([('bed.state', '=', 'occupied')])

    return occupied_bed


# List of hospital beds : TB
def fetch_list_beds() -> list:
    config.connect_to_gnu()

    my_model = Model.get('gnuhealth.inpatient.registration')
    hospital_beds = my_model.find(['bed', '!=', None])

    return hospital_beds


# Hospital discharges : A
def fetch_hospital_discharges() -> list:
    config.connect_to_gnu()

    my_model = Model.get('gnuhealth.inpatient.registration')
    discharges_patients = my_model.find([('state', '!=', 'hospitalized')])

    return discharges_patients


# List of patients administrated in intensive care : TI
def fetch_patients_icu() -> list:
    config.connect_to_gnu()

    my_model = Model.get('gnuhealth.inpatient.registration')
    patients_icu = my_model.find([('icu', '=', True)])

    return patients_icu


# Primary care discharges : PHC
def fetch_primary_care_discharges() -> list:
    config.connect_to_gnu()

    my_model = Model.get('gnuhealth.inpatient.registration')
    primary_evaluation = my_model.find([('discharge_reason', '=', 'home')])

    return primary_evaluation


# fetch notifiable and infectious disease
def fetch_notifiable_and_infectious_diseases() -> tuple:
    config.connect_to_gnu()

    my_model = Model.get('gnuhealth.pathology')

    infectious_diseases = my_model.find([('groups.disease_group.code', '=', 'INFECTIOUS')])
    notifiable_diseases = my_model.find([('groups.disease_group.code', '=', 'NOTIFIABLE')])

    unique_diseases = infectious_diseases[:]
    for disease in notifiable_diseases:
        if disease not in unique_diseases:
            unique_diseases.append(disease)

    return len(unique_diseases), unique_diseases


# fetch data Elements
def fetch_from_dhis2(api_url: str):
    try:
        r = s.get(api_url)
        if r.status_code == 200:
            result = r.json()
            return result
    except (requests.exceptions.ConnectionError, requests.exceptions.BaseHTTPError):
        raise error.APIError(f"Failed while fetching data elements.")


# fetch filtered notifiable and infectious diseases
def fetch_filtered_notifiable_and_infectious_diseases(filter_type: str, filter_value: str) -> tuple:
    config.connect_to_gnu()

    my_model = Model.get('gnuhealth.pathology')

    infectious_diseases, notifiable_diseases = [], []
    if filter_type == 'name':
        infectious_diseases = my_model.find([('groups.disease_group.code', '=', 'INFECTIOUS'),
                                             ['name', 'ilike', f"%{filter_value}%"]])
        notifiable_diseases = my_model.find([('groups.disease_group.code', '=', 'NOTIFIABLE'),
                                             ['name', 'ilike', f"%{filter_value}%"]])
    elif filter_type == 'code':
        infectious_diseases = my_model.find([('groups.disease_group.code', '=', 'INFECTIOUS'),
                                             ['code', 'ilike', f"%{filter_value}%"]])
        notifiable_diseases = my_model.find([('groups.disease_group.code', '=', 'NOTIFIABLE'),
                                             ['code', 'ilike', f"%{filter_value}%"]])

    unique_diseases = infectious_diseases[:]
    for disease in notifiable_diseases:
        if disease not in unique_diseases:
            unique_diseases.append(disease)

    return len(unique_diseases), unique_diseases


# fetch data indicators
def fetch_data_indicators():
    filename = "static/dataorg.csv"

    with open(filename) as f:
        reader = csv.reader(f)
        hearder_row = next(reader)

        indicators = [row[6] for row in reader if "IDS" in row[2]]
        unique_indicators = set(indicators)

        return unique_indicators


# send the new indicator created
def send_new_indicator(payload: dict, api_url: str):
    try:
        r = s.post(api_url, json=payload, headers={'Content-Type': 'application/json'})
        return r.json()
    except (requests.exceptions.HTTPError, requests.exceptions.RequestException,
            requests.exceptions.ConnectionError) as e:
        raise error.APIError(f"Error while sending the new indicator: {e}")


# write in indicator file
def store_data_indicator(data: dict):
    filename = "static/indicator.csv"

    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            header_row = reader.fieldnames

        with open(filename, 'a', newline='') as csvfile:
            fieldnames = [
                'diseaseId',
                'diseaseCode',
                'diseaseDisplayName',
                'indicatorDisplayName',
                'dataElementId',
                'dataElementDisplayName',
                'dataSetId',
                'dataSetPeriod',
                'createdDate'
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not header_row:
                writer.writeheader()

            writer.writerow(data)
    except FileNotFoundError:
        raise Exception("File not found")