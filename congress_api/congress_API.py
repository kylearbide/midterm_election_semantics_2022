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


#getting congressional based on chosen date
CONGRES_RECORD = 'congressional-record'
YEAR = '2022'
MONTH = '6'
DAY = '28'
endpoint = f"{CONGRES_RECORD}/?y={YEAR}&m={MONTH}&d={DAY}"

data,status_code = client.get(endpoint)

full_record_url = data['Results']['Issues'][0]['Links']['FullRecord']['PDF'][0]['Url']

# download file
rqs = Request(full_record_url,headers={"User-Agent": "Mozilla/5.0"})
resp = urlopen(rqs)
file = open(f"Congress_Records_{YEAR}-{MONTH}-{DAY}.pdf",'wb')
file.write(resp.read())
file.close()
print("completed")

"""
#getting range of dates and 
base=datetime.datetime.today()
date_list = [base-datetime.timedelta(days=x) for x in range(10)]

for day in date_list:
    day = day.day
    month = day.month
    year = day.year

"""
