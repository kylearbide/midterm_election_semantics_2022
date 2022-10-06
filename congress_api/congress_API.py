import requests
import sys
import os
import json
from cdg_client import CDGClient
import datetime
from urllib.request import Request,urlopen


with open(r'config.json', 'r') as f:
    CONFIG = json.load(f)
client = CDGClient(CONFIG['congress_API'])  # pass the key, response_format="xml" if needed

# use requests args and kwargs below modify the request:

def bill_test():
    BILL_HR = "hr"
    BILL_NUM = 21
    BILL_PATH = "bill"
    CONGRESS = 117

    endpoint = f"{BILL_PATH}/{CONGRESS}/{BILL_HR}/{BILL_NUM}/text"
    data, status_code = client.get(endpoint)

    print(data)

def congressional_record():
    endpoint = f"congressional-record/?y=2022&m=6&d=28"
    data, status_code = client.get(endpoint)

    print(data['Results']['Issues'][0]['Links']['FullRecord'])

congressional_record()
=======
BILL_HR = "hr"
BILL_NUM = 21
BILL_PATH = "bill"
CONGRESS = 117
NAME = 'Marco Rubio'

"""
go to package from PyMUPDF 'full record' from json data go back before the bills we are looking at
august 7 climate bill: https://www.cfr.org/in-brief/us-climate-bill-inflation-reduction-act-gets-right-wrong-emissions back to the beginning of June 
go through JSON file and put it in github

"""
endpoint = f"{BILL_PATH}/{CONGRESS}/{BILL_HR}/{BILL_NUM}/text"
data, status_code = client.get(endpoint)





"""
getting range of dates starting from July 7-September 7 (August 7 was climate bill).
This will give us all records in 2 month span with climate bill in the middle
"""
base=datetime.datetime(2022,9,7)
date_list = [base-datetime.timedelta(days=x) for x in range(61)]
for day in date_list:
    d = day.day
    m = day.month
    y = day.year
    #getting congressional based on chosen date

    CONGRES_RECORD = 'congressional-record'
    endpoint = f"{CONGRES_RECORD}/?y={y}&m={m}&d={d}"
    data,status_code = client.get(endpoint)
    issues = data['Results']['Issues']
    if len(issues)==0:
        print("no records for this day")
    else:
        full_record_url = data['Results']['Issues'][0]['Links']['FullRecord']['PDF'][0]['Url']

        # download file
        rqs = Request(full_record_url,headers={"User-Agent": "Mozilla/5.0"})
        resp = urlopen(rqs)
        file = open(f"Congressional Records/Congress_Records_{y}-{m}-{d}.pdf",'wb')
        file.write(resp.read())
        file.close()
        print("completed")

