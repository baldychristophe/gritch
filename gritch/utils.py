import datetime


def format_datetime(datetime_arg: datetime.datetime):
    return datetime_arg.strftime('%B %d, %Y, %H:%M:%S')
