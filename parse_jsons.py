import pandas as pd
from pandas.io.json import json_normalize
import json
import glob

dflist=[]

for g in glob.glob("full_contact_responses/*/*.json"):

	print g
	f=json.load(open(g))

	name=g.split("/")[-1][:-5]

	try:
		j=json_normalize(f["socialProfiles"])
		j["Email"]=name
		dflist.append(j)
	except:
		continue

df=pd.concat(dflist)

df.to_csv("results.csv", index=False, encoding="utf-8")
