from datetime import date, datetime

import pytz


def get_first_name(name_obj):
    if name_obj is None:
        return None
    first_name = str(name_obj).split(" ")[0]
    return first_name


def get_username(email_obj):
    if email_obj is None:
        return None
    username = str(email_obj).split("@")[0]
    return username


def str_to_date(date_str: str):
    if date_str is None:
        return None
    if isinstance(date_str, date):
        return date_str

    dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return dt_obj.date()


def str_to_datetime(datetime_str: str):
    if datetime_str is None:
        return None
    if isinstance(datetime_str, datetime):
        return datetime_str

    dt_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt_obj


def dt_to_br_timezone(datetime_obj: datetime):
    if isinstance(datetime_obj, datetime) is False:
        return datetime_obj

    utc_tz = pytz.utc
    br_tz = pytz.timezone("America/Sao_Paulo")

    utc_dt = utc_tz.localize(datetime_obj)
    br_dt = utc_dt.astimezone(br_tz)
    return br_dt
