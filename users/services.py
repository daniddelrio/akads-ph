import requests, os, json
from requests.auth import HTTPBasicAuth
from decouple import config

API_URL = "https://api.paymongo.com/v1"

CURRENCY = "PHP"
RATE_FIRST_HOUR = 700
RATE_FIRST_HALF_HOUR = RATE_FIRST_HOUR // 2
RATE_SUCCEEDING = 600
RATE_SUCCEEDING_HALF = RATE_SUCCEEDING // 2


def create_token(number, exp_month, exp_year, cvc):
    url = os.path.join(API_URL, "tokens")
    data = {
        "data": {
            "attributes": {
                "number": str(number),
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": str(cvc),
                "billing": {},
            }
        }
    }
    res = requests.post(
        url, json=data, auth=HTTPBasicAuth(config("PAYMONGO_PUBLIC_KEY"), "")
    )
    token_data = res.json()
    return token_data


def retrieve_token(token_id):
    url = os.path.join(API_URL, "tokens", token_id)
    res = requests.get(url, auth=HTTPBasicAuth(config("PAYMONGO_PUBLIC_KEY"), ""))
    token_data = res.json()
    return token_data


def get_amount_from_minutes(minutes):
    hours = minutes // 60
    amount = 0

    if hours == 1:
        amount += RATE_FIRST_HOUR
    elif hours > 1:
        amount += RATE_FIRST_HOUR
        amount += RATE_SUCCEEDING * (hours - 1)

    remaining_minutes = minutes - (hours * 60)
    if remaining_minutes >= 45:
        if hours == 0:
            amount += RATE_FIRST_HOUR
        else:
            amount += RATE_SUCCEEDING
    elif remaining_minutes >= 15:
        if hours == 0:
            amount += RATE_FIRST_HALF_HOUR
        else:
            amount += RATE_SUCCEEDING_HALF

    return amount


# Minutes is the duration of the tutoring session
def create_payment(token_id, amount, tutor_name, date):
    url = os.path.join(API_URL, "payments")

    data = {
        "data": {
            "attributes": {
                # Convert Pesos to Centavos
                "amount": amount * 100,
                "currency": CURRENCY,
                "description": "Payment for your tutoring session on {} with {}".format(
                    date, tutor_name
                ),
                "source": {"id": token_id, "type": "token"},
            }
        }
    }
    res = requests.post(
        url, json=data, auth=HTTPBasicAuth(config("PAYMONGO_SECRET_KEY"), "")
    )
    payment_data = res.json()
    return payment_data
