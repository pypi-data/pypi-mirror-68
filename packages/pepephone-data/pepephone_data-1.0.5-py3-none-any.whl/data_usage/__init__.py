#!/usr/bin/env python3

import calendar
import configparser
import datetime
import os
import pathlib

import requests


def read_configuration():
    config_home = os.path.join(str(pathlib.Path.home()), ".pepephone")
    config_system = os.path.join("/etc", "pepephone")

    config = configparser.ConfigParser()
    if os.path.isfile(config_home):
        config.read(config_home)
    else:
        config.read(config_system)

    return config


def read_configuration_authentication():
    return read_configuration()["authentication"]


def read_configuration_extra():
    configuration = read_configuration()
    if 'extra' in configuration:
        return configuration['extra']
    else:
        return None


def read_configuration_extra_GB():
    configuration_extra = read_configuration_extra()

    if configuration_extra and 'extra_GB' in configuration_extra:
        return int(configuration_extra['extra_GB'])
    else:
        return 0


def get_authorization_code():
    """
    POST to https://services.pepephone.com/v1/auth with parameters:
    JSON with email, password and source: ECARE_WEB.
    Returns authorization code
    """

    authentication_data = read_configuration_authentication()
    print("Getting authorization code...")
    payload = {"email": authentication_data["email"], "password": authentication_data["password"],
               "source": "ECARE_WEB"}
    json_request = requests.post("https://services.pepephone.com/v1/auth", json=payload).json()
    return json_request["jwt"]


def get_consumption(authorization_code):
    """
    GET https://services.pepephone.com/v1/consumption/623040167, pass
    Authorization: Bearer and the Authorization code
    """
    print("Getting consumption...")
    headers = {"Authorization": "Bearer {}".format(authorization_code)}
    authentication = read_configuration_authentication()
    consumption = requests.get("https://services.pepephone.com/v1/consumption/{}".format(authentication["phone"]),
                               headers=headers)
    return consumption.json()


def calculate_total_data_gb(consumption_json):
    total = consumption_json["dataFlat"]

    if "bundles" in consumption_json:
        for bundle in consumption_json["bundles"]:
            total += bundle["data"]

    return total / 1024


def main():
    if 'REQUEST_METHOD' in os.environ:
        print("Content-Type: text/plain\n")

    authorization_code = get_authorization_code()
    consumption_json = get_consumption(authorization_code)

    print()
    data_consume_all_gb = (consumption_json["dataConsumeAll"] + consumption_json["dataConsumeRoamingRlah"]) / 1024
    data_consume_eu_gb = consumption_json["dataConsumeRoamingRlah"] / 1024
    data_total_available_gb = calculate_total_data_gb(consumption_json)

    extra_GB = read_configuration_extra_GB()
    if extra_GB > 0:
        extra_message = f'(Including extra {extra_GB} GB)'
    else:
        extra_message = ''

    data_total_available_gb += extra_GB

    now = datetime.datetime.now()
    data_remaining = data_total_available_gb - data_consume_all_gb
    number_of_days_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days_month = (number_of_days_month - now.day) + 1

    print("Time         : {}".format(now.strftime("%Y-%m-%d %H:%M:%S")))
    print("GB total     : {:.2f} GB {}".format(data_total_available_gb, extra_message))
    print()
    print("GB used total: {:.2f} GB (EU roaming: {:.2f} GB)".format(data_consume_all_gb, data_consume_eu_gb))
    print("GB used/day  : {:.2f} GB/day".format(data_consume_all_gb / now.day))
    print()
    print("GB remaining : {:.2f} GB".format(data_total_available_gb - data_consume_all_gb))
    print("GB remain/day: {:.2f} GB/day".format(data_remaining / remaining_days_month))
    print()

    percentage_used = (data_consume_all_gb / data_total_available_gb) * 100
    print("% Used       : {:.2f}%".format(percentage_used))

    percentage_month = (now.day / number_of_days_month) * 100
    print("% Month      : {:.2f}%".format(percentage_month))


if __name__ == "__main__":
    main()