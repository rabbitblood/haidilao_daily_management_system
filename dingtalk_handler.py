import requests

APP_KEY_AND_SECRET = {"appkey":"dinguzubg4nrrftnts3o",
					  "appsecret":"0hdMQ5-3vuZU-nr9jCsVz7IXikh0IbUTenJi6g5-rzqZ-F4QJno8l_wqUS7q-tGG"}

access_token = requests.get("https://oapi.dingtalk.com/gettoken", APP_KEY_AND_SECRET).json()["access_token"]


