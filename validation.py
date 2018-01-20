import datetime


def validate_date_input(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False

    return True


def validate_time_spent(time):
    try:
        int(time)
    except ValueError:
        return False

    return True
