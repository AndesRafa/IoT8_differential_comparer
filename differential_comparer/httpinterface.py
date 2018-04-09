import requests


def get(url, params):
    return requests.get(url, params)


def post(url, data, json):
    return requests.post(url, data, json)
