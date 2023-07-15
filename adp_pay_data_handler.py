import requests


def get_pay_data_from_adp():
    current_session = requests.session()

    payload = {"identifier": "154772610"}

    current_request = current_session.post("https://online.adp.com/api/sign-in-service/v1/sign-in.account.identify", json=payload)
    print(current_request.content)


if __name__ == "__main__":
    get_pay_data_from_adp()
