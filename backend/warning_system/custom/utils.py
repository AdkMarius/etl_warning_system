from datetime import datetime


def get_previous_date():
    current_day = datetime.now()
    previous_day = datetime(current_day.year, current_day.month, current_day.day - 1)

    return previous_day


def date_and_period():
    previous_day = get_previous_date()
    period = previous_day.strftime("%Y%m%d")

    return previous_day, period


def weekly_period():
    today_date = datetime.now()
    week_number = today_date.isocalendar()
    period = str(week_number.year) + "W" + str(week_number.week - 1)

    return today_date, period

