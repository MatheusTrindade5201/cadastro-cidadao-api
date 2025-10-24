import pytz
from datetime import datetime

local_timezone = pytz.timezone("America/Sao_Paulo")


def utc_to_local(utc_dt):
    if not isinstance(utc_dt, datetime):
        raise TypeError("utc_to_local espera um objeto datetime.")
    return (
        utc_dt.replace(tzinfo=pytz.utc)
        .astimezone(local_timezone)
        .replace(tzinfo=None)
    )
