#!/usr/bin/python
import os
import sys
import time
import logging
import tailhead
import requests
import argparse
from pprint import pprint

# module_path = os.path.abspath(os.path.join('.'))
# if module_path not in sys.path:
#     sys.path.append(module_path)


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# -------------------------------------------------------------------------
# INPUT ARGS

parser = argparse.ArgumentParser(description='zabbix-rt-export-tailer - tail zabbix rt export logs and forward them to an HTTP API')

parser.add_argument("--export-file", type=str, required=True,
                    help="Full path of input RT export file")
parser.add_argument("--api-url", type=str, required=True,
                    help="URL of API to forward logs to")
parser.add_argument("--proxy", type=str, required=False,
                    help="HTTP proxies")

parsed = parser.parse_args()

file_path = parsed.export_file
api_url = parsed.api_url
proxy = parsed.proxy



# -------------------------------------------------------------------------
# MAIN

for line in tailhead.follow_path(file_path):
    if line is None:
        time.sleep(0.1)
        continue

    try:
        proxies_dict = {}
        if proxy:
            proxies_dict = {
                "http"  : proxy,
                "https" : proxy,
            }

        resp = requests.post(api_url,
                             data=line,
                             headers={'Content-Type': 'application/json'},
                             proxies=proxies_dict)

        # try:
        #     r.raise_for_status()
        # except requests.exceptions.HTTPError as e:
        #     return False

        resp.close()
    except requests.RequestException as e:
        pass
