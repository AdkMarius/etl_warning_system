from datetime import datetime

from warning_system.models.datas import *
from warning_system.custom import utils


# Count a number of disease according the kind of disease
# record_type is boolean to determine weather records is diseases or deaths
# True for diseases and False for deaths
def count_records(records: list, code: str, record_type: str) -> int:
    count = 0
    match record_type:
        case 'DISEASE':
            for record in records:
                if record.pathology.code == code:
                    count += 1
        case 'DEATH':
            for record in records:
                if record.cod.code == code:
                    count += 1
        case 'INPATIENT_REGISTRATION':
            for record in records:
                if record.admission_reason.code == code:
                    count += 1

    return count


# Get records created in this day
def get_daily_records(records: list, instant: datetime) -> list:
    daily_records = []
    daily_date = instant.date()
    for record in records:
        create_date = record.create_date.date()
        if create_date == daily_date:
            daily_records.append(record)

    return daily_records


def confirmed_cases(code: str) -> int:
    confirmed_diseases = fetch_confirmed_diseases()
    count = count_records(confirmed_diseases, code, 'DISEASE')

    return count


def recovered_cases(code: str) -> int:
    recovered_diseases = fetch_recovered_diseases()
    count = count_records(recovered_diseases, code, 'DISEASE')

    return count


def suspected_cases(code: str) -> int:
    suspected_diseases = fetch_suspected_diseases()
    count = count_records(suspected_diseases, code, 'DISEASE')

    return count


def get_deaths(code: str) -> int:
    deaths = fetch_deaths()
    count = count_records(deaths, code, 'DEATH')

    return count


# A
def get_hospital_discharges(code: str) -> int:
    hospital_discharges = fetch_hospital_discharges()
    count = count_records(hospital_discharges, code, 'INPATIENT_REGISTRATION')

    return count


# IT
def get_patients_icu(code: str) -> int:
    patients_icu = fetch_patients_icu()
    count = count_records(patients_icu, code, 'INPATIENT_REGISTRATION')

    return count


# B
def get_occupied_beds(code: str) -> int:
    occupied_beds = fetch_occupied_bed()
    count = count_records(occupied_beds, code, 'INPATIENT_REGISTRATION')

    return count


# BT
def hospital_beds(code: str) -> int:
    beds = fetch_list_beds()
    count = count_records(beds, code, 'INPATIENT_REGISTRATION')

    return count


# PHC
def get_primary_care_discharges(code: str) -> int:
    primary_care_discharges = fetch_primary_care_discharges()
    count = count_records(primary_care_discharges, code, 'INPATIENT_REGISTRATION')

    return count


# Solved
def solved_result(code: str) -> int:
    solved = recovered_cases(code) + get_deaths(code)

    return solved


# Active Cases
def active_cases(code: str) -> int:
    count = confirmed_cases(code) - recovered_cases(code) - get_deaths(code)

    return count


# Recovered percentage
def recovered_percentage(code: str) -> int:
    percentage = 0
    try:
        percentage = (recovered_cases(code) // confirmed_cases(code)) * 100
    except ZeroDivisionError:
        pass

    return percentage


# Death percentage
def deaths_percentage(code: str) -> int:
    percentage = 0
    try:
        percentage = (get_deaths(code) // confirmed_cases(code)) * 100
    except ZeroDivisionError:
        pass

    return percentage


# Daily confirmed cases
def daily_confirmed_cases(code: str) -> int:
    confirmed_diseases = fetch_confirmed_diseases()
    daily_confirmed = get_daily_records(confirmed_diseases, datetime.now())

    count = count_records(daily_confirmed, code, 'DISEASE')
    return count


# Return the number of recovered diseases based on the date
def day_recovered_cases(code: str, instant: datetime) -> int:
    recovered_diseases = fetch_recovered_diseases()
    daily_recovered = get_daily_records(recovered_diseases, instant)

    count = count_records(daily_recovered, code, 'DISEASE')
    return count


# Daily recovered cases
def daily_recovered_cases(code: str) -> int:
    count = day_recovered_cases(code, datetime.now())
    return count


# Daily Death
def daily_deaths_cases(code: str) -> int:
    deaths = fetch_deaths()
    daily_deaths = get_daily_records(deaths, datetime.now())

    count = count_records(daily_deaths, code, 'DEATH')
    return count


# Daily Solved
def daily_solved_cases(code: str) -> int:
    daily_solved = daily_recovered_cases(code) + daily_deaths_cases(code)
    return daily_solved


# Pre Active Cases
def get_pre_active_cases(code: str) -> int:
    previous_date = utils.get_previous_date()
    pre_active_cases = confirmed_cases(code) - get_deaths(code) - day_recovered_cases(code, previous_date)

    return pre_active_cases


# aHSI
def get_ahsi(code: str) -> int:
    ahsi = (suspected_cases(code) // confirmed_cases(code)) * 100
    return ahsi


# dHSI
def get_dhsi(code: str) -> int:
    dhsi = daily_solved_cases(code) // daily_confirmed_cases(code)
    return dhsi


# hPOR
def get_hpor(code: str) -> int:
    hpor = get_pre_active_cases(code) // hospital_beds(code)
    return hpor


# icuPOR
def get_icu_por(code: str) -> int:
    icu_por = get_pre_active_cases(code) // get_patients_icu(code)
    return icu_por


# calculate new indicator
def calculate_new_indicator(indicator: str, code: str) -> int:
    result = 0
    match indicator:
        case 'SUSPECTED': result = suspected_cases(code)
        case 'CONFIRMED': result = confirmed_cases(code)
        case 'RECOVERED': result = recovered_cases(code)
        case 'DEATHS': result = get_deaths(code)
        case 'A': result = get_hospital_discharges(code)
        case 'B': result = get_occupied_beds(code)
        case 'BT': result = hospital_beds(code)
        case 'IT': result = get_patients_icu(code)
        case 'ACTIVECASEST': result = active_cases(code)
        case 'PREACTIVECASEST': result = get_pre_active_cases(code)
        case 'SOLVEDT': result = solved_result(code)
        case 'DEATHSPERCENTAGET': result = deaths_percentage(code)
        case 'RECOVEREDPERCENTAGET': result = recovered_percentage(code)
        case 'AHSI': result = get_ahsi(code)
        case 'DHSI': result = get_dhsi(code)
        case 'HPORT': result = get_hpor(code)
        case 'ICUPORR': result = get_icu_por(code)
        case 'PHC': result = get_primary_care_discharges(code)
        case 'DAILYCONFIRMEDT': result = daily_confirmed_cases(code)
        case 'DAILYRECOVEREDT': result = daily_recovered_cases(code)
        case 'DAILYDEATH': result = daily_deaths_cases(code)
        case 'DAILYSOLVEDT': result = daily_solved_cases(code)

    return result

