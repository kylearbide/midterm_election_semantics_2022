import requests
import sys
import os
import json
from cdg_client import CDGClient
import datetime
from urllib.request import Request,urlopen
import fitz
import pdfplumber
import matplotlib.pyplot as plt 
import os
import re 
import pandas as pd
import selenium as se

"""
grabbing congressional records since 2020-01-01. Creates date range with dates that aren't in the
2 month period we initially grabbed data from (july 07-September 07), and grabs data from those dates
"""



# Candidate dictionary 
candidatedict = [{'Name':'Ron Johnson','Party':'Republican','BIOGUIDEID':'J000293','State':'Wisconsin',"Winning Prob":[60]},
{'Name':'Mandela Barnes','Party':'Democrat','BIOGUIDEID':'-','State':'Wisconsin',"Winning Prob":[40]},{'Name':'Catherine Cortez Masto','Party':'Democrat','BIOGUIDEID':'C001113','State':'Nevada',"Winning Prob":[56]},
{'Name':'Adam Paul Laxalt','Party':'Republican','BIOGUIDEID':'L000148','State':'Nevada',"Winning Prob":[44]},{'Name':'Mark Kelly','Party':'Democrat','BIOGUIDEID':'K000377','State':'Arizona',"Winning Prob":[84]},
{'Name':'Blake Masters','Party':'Republican','BIOGUIDEID':'-','State':'Arizona',"Winning Prob":[16]},{'Name':'Marco Rubio','Party':'Republican','BIOGUIDEID':'R000595','State':'Florida',"Winning Prob":[85]},
{'Name':'Val Demings','Party':'Democrat','BIOGUIDEID':'D000627','State':'Florida',"Winning Prob":[15]},{'Name':'Raphael Warnock','Party':'Democrat','BIOGUIDEID':'W000790','State':'Georgia',"Winning Prob":[55]},
{'Name':'Herschel Junior Walker','Party':'Republican','BIOGUIDEID':'-','State':'Georgia',"Winning Prob":[45]},{'Name':'Tedd Budd','Party':'Republican','BIOGUIDEID':'B001305','State':'North Carolina',"Winning Prob":[62]},
{'Name':'James David Vance','Party':'Republican','BIOGUIDEID':'-','State':'Ohio',"Winning Prob":[72]},{'Name':'Cheri Beasley','Party':'Democrat','BIOGUIDEID':'-','State':'North Carolina',"Winning Prob":[38]},
{'Name':'Tim Ryan','Party':'Democrat','BIOGUIDEID':'R000577','State':'Ohio',"Winning Prob":[28]},{'Name':'Wiley Nickel','Party':'Democrat','BIOGUIDEID':'-','State':'North Carolina',"Winning Prob":[46]},
{'Name':'John Fetterman','Party':'Democrat','BIOGUIDEID':'-','State':'Pennsylvania',"Winning Prob":[81]},{'Name':'Bo Hines','Party':'Republican','BIOGUIDEID':'-','State':'North Carolina',"Winning Prob":[54]},
{'Name':'Mehmet Oz','Party':'Republican','BIOGUIDEID':'-','State':'Pennsylvania',"Winning Prob":[19]},{'Name':'Yvette Herrell','Party':'Republican','BIOGUIDEID':'H001084','State':'New-Mexico',"Winning Prob":[40]},
{'Name':'Maggie Hassan','Party':'Democrat','BIOGUIDEID':'H001076','State':'New Hampshire',"Winning Prob":[86]},{'Name':'Gabriel Vasquez','Party':'Democrat','BIOGUIDEID':'-','State':'New-Mexico',"Winning Prob":[40]},
{'Name':'Donald C. Bolduc','Party':'Republican','BIOGUIDEID':'-','State':'New Hampshire',"Winning Prob":[14]},{'Name':'April Becker','Party':'Republican','BIOGUIDEID':'-','State':'Nevada',"Winning Prob":[35]},
{'Name':'Mike Lee','Party':'Republican','BIOGUIDEID':'-','State':'Utah',"Winning Prob":[93]},{'Name':'Susie Lee','Party':'Democrat','BIOGUIDEID':'L000590','State':'Nevada',"Winning Prob":[65]},
{'Name':'Evan McMullin','Party':'Independent','BIOGUIDEID':'-','State':'Utah',"Winning Prob":[7]},{'Name':'Tyler Kistner','Party':'Republican','BIOGUIDEID':'-','State':'Minnesota',"Winning Prob":[31]},
{'Name':'Sarah Palin','Party':'Republican','BIOGUIDEID':'-','State':'Alaska',"Winning Prob":[46]},{'Name':'Angie Craig','Party':'Democrat','BIOGUIDEID':'C001119','State':'Minnesota',"Winning Prob":[69]},
{'Name':'Mary S. Peltola','Party':'Democrat','BIOGUIDEID':'P000619','State':'Alaska',"Winning Prob":[39]},{'Name':'Neil C. Parrott','Party':'Democrat','BIOGUIDEID':'-','State':'Maryland',"Winning Prob":[41]},
{'Name':'Mark Begich','Party':'Republican','BIOGUIDEID':'B001265','State':'Alaska',"Winning Prob":[15]},{'Name':'David J Trone','Party':'Republican','BIOGUIDEID':'T000483','State':'Maryland',"Winning Prob":[59]},
{'Name':'Eli Crane','Party':'Republican','BIOGUIDEID':'-','State':'Arizona',"Winning Prob":[66]},{'Name':'Bruce Poliquin','Party':'Republican','BIOGUIDEID':'P000611','State':'Maine',"Winning Prob":[47]},
{'Name':"Tom O'Halleran",'Party':'Democrat','BIOGUIDEID':'O000171','State':'Arizona',"Winning Prob":[34]},{'Name':'Jared Forest Golden','Party':'Democrat','BIOGUIDEID':'G000592','State':'Maine',"Winning Prob":[53]},
{'Name':'Barbara Kirkmeyer','Party':'Republican','BIOGUIDEID':'-','State':'Colorado',"Winning Prob":[56]},{'Name':'Sharice Davids','Party':'Democrat','BIOGUIDEID':'D000629','State':'Kansas',"Winning Prob":[47]},
{'Name':'Yadira Caraveo','Party':'Democrat','BIOGUIDEID':'-','State':'Colorado',"Winning Prob":[44]},{'Name':'Amanda L. Adkins','Party':'Republican','BIOGUIDEID':'-','State':'Kansas',"Winning Prob":[53]},
{'Name':'Eric Sorensen','Party':'Democrat','BIOGUIDEID':'-','State':'Illinois',"Winning Prob":[54]},{'Name':'Esther Joy King','Party':'Republican','BIOGUIDEID':'-','State':'Illinois',"Winning Prob":[46]}]

canddf = pd.DataFrame()
for cand in candidatedict:
    print(cand['Name'])
    c = pd.DataFrame.from_dict(cand)
    ls = [canddf,c]
    canddf = pd.concat(ls)

"""
Figures for Capstone Plan 2 Presentation
fig,ax = plt.subplots()
canddf = canddf.rename({'Winning Prob':'Likelihood'},axis='columns')
withoutindependent = canddf.loc[(canddf['Party']=='Republican') | (canddf['Party']=='Democrat')]
groups = withoutindependent.groupby('Party')

print(groups)

for Party,group in groups:
    ax.plot(group.State,group.Likelihood, marker='o', linestyle='', ms=12, label=Party)
    ax.legend
ax.legend()
ax2 = withoutindependent['Likelihood'].hist(by=withoutindependent['Party'])

for ax in ax2.flatten():
    ax.set_xlabel('Win Probability %')
    ax.set_ylabel('Count')
plt.ylim(0,5)
plt.show()


"""






with open(r'config.json', 'r') as f:
    CONFIG = json.load(f)
client = CDGClient(CONFIG['congress_API'])  # pass the key, response_format="xml" if needed

# use requests args and kwargs below modify the request:
BILL_HR = "hr"
BILL_NUM = 21
BILL_PATH = "bill"
CONGRESS = 117


"""
go to package from PyMUPDF 'full record' from json data go back before the bills we are looking at
august 7 climate bill: https://www.cfr.org/in-brief/us-climate-bill-inflation-reduction-act-gets-right-wrong-emissions back to the beginning of June 
go through JSON file and put it in github

"""
endpoint = f"{BILL_PATH}/{CONGRESS}/{BILL_HR}/{BILL_NUM}/text"
data, status_code = client.get(endpoint)

"""
iterate over list using package spaacy 
"""


"""
write records as text
"""
direct = os.listdir('Congressional Records')
for record in direct:
    txtname=record[0:-4]
    doc = fitz.open(f"Congressional Records/{record}")
    txt = ''
    no_pages = len(doc)
    print(no_pages)
    for i in range(0,no_pages):
        page = doc[i]
        txt += page.get_text()
        txt+=f"\n -Page {i}-\n"
    with open(f"Records as txt/{txtname}.txt",'w') as f:
        f.write(txt)
    





"""
getting range of dates starting from July 7-September 7 (August 7 was climate bill).
This will give us all records in 2 month span with climate bill in the middle
"""
daterange = pd.date_range(start="2021-02-16",end=datetime.datetime.today())
base=datetime.datetime(2022,9,7)
date_list = [base-datetime.timedelta(days=x) for x in range(61)]
daterange = list(pd.to_datetime(daterange).to_series())

for day in date_list:
    if day in daterange:
        daterange.remove(day)
for day in daterange:
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

