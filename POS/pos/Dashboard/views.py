import datetime
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
import json

# logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)
default_http_headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


def Dashboard(request, rxuid):
    API_URL = 'https://CCR-TESTBENCH:5000/{}/{}'
    template = loader.get_template('Dashboard.html')

    method = 'getselectedticker'
    body = {
        'userid': rxuid,
    }
    selectedticker = post(API_URL.format('Account', rxuid), method, body)['data']['selectedticker']

    user = {
        'uid': rxuid,
        'selectedticker': selectedticker
    }

    context = {
        'user': user
    }
    return HttpResponse(template.render(context, request))


def reload(request):
    return Dashboard(request)


def post(url, method, body, headers=None):
    if headers is None:
        headers = default_http_headers
    data = {'method': method, 'body': body}
    return requests.post(url, data=json.dumps(data), headers=headers, verify=False).json()
