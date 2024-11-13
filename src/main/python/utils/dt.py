import datetime


def get_today():
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y")


def get_day_offset(offset, dt=False):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=offset)
    curr = now + delta
    if dt:
        return curr
    return curr.strftime("%m/%d/%Y")
