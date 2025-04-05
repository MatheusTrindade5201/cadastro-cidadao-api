import pytz

local_timezone = pytz.timezone("America/Sao_Paulo")


def utc_to_local(utc_dt):
    return (
        utc_dt.replace(tzinfo=pytz.utc)
        .astimezone(local_timezone)
        .replace(tzinfo=None)
    )
