# -*- coding: utf-8 -*-
"""
@Author    : Jess
@Email     : 2482003411@qq.com
@License   : Copyright(C), Jess
@Time      : 2020/4/29 18:37
@File      : api.py
@Version   : 1.0
@Description: 
"""
import json
import logging

import requests

from src.main.utils import get_default_logger

DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_TIMEOUT = ""

log = get_default_logger(__name__)


class MyRequest(object):
    @staticmethod
    def get(url, params=None, headers=None):
        """
        """
        try:
            response = requests.request('GET', url=url, params=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print('Received response with no content', response.json())
        except Exception as e:
            print(e)

    @staticmethod
    def post(url, data=None, headers=None, files=None):
        try:
            response = requests.request('POST', url=url, json=data, headers=headers, files=files)
            if response.status_code >= 200 and response.status_code < 300:
                return response.json()
            else:
                print(response.json())
        except Exception as e:
            print(e)

    @staticmethod
    def put(url, data=None, headers=None, files=None):
        try:
            response = requests.request('PUT', url=url, json=data, headers=headers, files=files)
            if response.status_code >= 200 and response.status_code < 300:
                return response.json()
            else:
                print(response.json())
        except Exception as e:
            print(e)


def school_login(email, password):
    url = DEFAULT_BASE_URL + "/v1/api/schools/login"

    payload = {
        "email": email,
        "password": password
    }

    headers = {
        'Content-Type': "application/json"
    }

    response = MyRequest.post(url=url, data=payload, headers=headers)
    return response

def get_cert(cert_id, api_token):
    url = DEFAULT_BASE_URL + "/v1/api/school_certificates/" + cert_id + "/"

    headers = {
        'Content-Type': "application/json",
        'API-HTTP-AUTHORIZATION': api_token
    }

    response = MyRequest.get(url=url, headers=headers)

    return response

def get_cert_detail(cert_id, api_token):
    url = DEFAULT_BASE_URL + "/v1/api/school_certificates/"+ cert_id + "/detail"
    headers = {
        'Content-Type': "application/json",
        'API-HTTP-AUTHORIZATION': api_token
    }
    response = MyRequest.get(url=url, headers=headers)
    response["unsign_cert"]["badge"]["image"] = response["unsign_cert"]["badge"]["image"].replace(DEFAULT_BASE_URL, "")
    response["unsign_cert"]["badge"]["issuer"]["id"] = response["unsign_cert"]["badge"]["issuer"]["id"].replace(DEFAULT_BASE_URL, "")
    response["unsign_cert"]["badge"]["issuer"]["revocationList"] = response["unsign_cert"]["badge"]["issuer"]["revocationList"].replace(DEFAULT_BASE_URL, "")
    return response

def cert_issue(cert_id, api_token, block_cert, tx_id, chain):
    url = DEFAULT_BASE_URL + "/v1/api/school_certificates/"+cert_id+"/issue/"
    headers = {
        'Content-Type': "application/json",
        'API-HTTP-AUTHORIZATION': api_token
    }
    data = {
        "block_cert": block_cert,
        "tx_id": tx_id,
        "chain": chain
    }
    response = MyRequest.post(url=url, data=data, headers=headers)
    return response