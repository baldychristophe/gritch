import datetime


def format_datetime(datetime_arg: datetime.datetime):
    return datetime_arg.strftime('%B %d, %Y, %H:%M:%S')


def truncate_commit_message(string: str, max_length: int):
    message_parts = string.split('\n')
    message_preview = message_parts[0]

    if len(message_preview) <= max_length:
        return message_preview
    return f'{message_preview[:max_length]}...'
