import datetime
from dateutil.relativedelta import relativedelta


def users_processor(request):
    start_date = datetime.date(year=2020, month=3, day=1)
    # Inclusive
    end_date = datetime.date(year=2022, month=12, day=1)
    increment = relativedelta(months=1)

    expiry_date_range = []
    while start_date <= end_date:
        expiry_date_range.append(start_date.strftime("%m/%Y"))
        start_date += increment

    return {"expiry_date_range": expiry_date_range}
