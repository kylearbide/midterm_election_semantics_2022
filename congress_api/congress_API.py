import requests
import sys
import os
import json
from cdg_client import CDGClient

with open(r'C:\Users\thatb\OneDrive\Desktop\Fall 2022\Data Driven Policy\election_candidate_sematics\midterm_election_semantics_2022\config.json', 'r') as f:
    CONFIG = json.load(f)
client = CDGClient(CONFIG['congress_API'])  # pass the key, response_format="xml" if needed

# use requests args and kwargs below modify the request:
BILL_HR = "hr"
BILL_NUM = 21
BILL_PATH = "bill"
CONGRESS = 117

endpoint = f"{BILL_PATH}/{CONGRESS}/{BILL_HR}/{BILL_NUM}/text"
data, status_code = client.get(endpoint)

print(data)