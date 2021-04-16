#!/usr/bin/python
import os
import sys
import logging
import tailhead
import requests
import argparse
from pprint import pprint

# module_path = os.path.abspath(os.path.join('.'))
# if module_path not in sys.path:
#     sys.path.append(module_path)


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# -------------------------------------------------------------------------
# INPUT ARGS

parser = argparse.ArgumentParser(description='zabbix-rt-export-tailer - tail zabbix rt export logs and forward them to an HTTP API')

parser.add_argument("--export-file", type=str, required=True,
                    help="Full path of input RT export file")
parser.add_argument("--api-url", type=str, required=True,
                    help="URL of API to forward logs to")
parser.add_argument("--proxies", type=str, required=True,
                    help="HTTP proxies")

parsed = parser.parse_args()

file_path = parsed.export_file
api_url = parsed.api_url
proxies = parsed.proxies



# -------------------------------------------------------------------------
# MAIN

for line in tailhead.follow_path(file_path):
    try:
        resp = requests.post(api_url, data=line
                             headers={'Content-Type': 'application/json'})

        # try:
        #     r.raise_for_status()
        # except requests.exceptions.HTTPError, e:
        #     return False

        resp.close()
    except requests.RequestException, e:
        pass
