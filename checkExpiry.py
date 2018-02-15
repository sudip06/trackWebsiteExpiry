#!/usr/bin/python3

import whois
from datetime import datetime
from sys import argv,exit
import pandas as pd
import numpy as np
import os.path

def calculateDaysToExpire(ExpiryDate):
	differenceTime=datetime.strptime(ExpiryDate,'%d/%m/%Y')-datetime.now()
	return differenceTime.days

now = datetime.now()
with open('fileList.dat') as f:
	content=f.readlines()
	content=[x.strip() for x in content]
	if(os.path.exists("out.csv")):
		df=pd.read_csv('out.csv', sep='\t', encoding='utf-8', index_col='Domain')
	else:
		df=pd.DataFrame(columns=['Domain','Days to expire',"Expiry Date"])
		df.set_index('Domain') 

	for domain in content:
		if (domain not in df.index) or(np.isnan(df.at[domain,'Days to expire'])):
			try:
				w = whois.whois(domain)

				if (w.expiration_date and w.status) == None:
					days_to_expire=np.nan
					domain_expiration_date=np.nan

				elif (type(w.expiration_date) == list):
					w.expiration_date = w.expiration_date[0]
					timedelta = w.expiration_date - now
					days_to_expire = timedelta.days
					domain_expiration_date=w.expiration_date
				else:
					domain_expiration_date = str(w.expiration_date.day) + '/' + str(w.expiration_date.month) + '/' + str(w.expiration_date.year)
				if not np.isnan(days_to_expire):
					timedelta = w.expiration_date - now
					days_to_expire = timedelta.days

			except (whois.parser.PywhoisError):
					days_to_expire=np.nan
					domain_expiration_date=np.nan
			#df=df.append({'Domain':domain, 'Days to expire':days_to_expire, 'Expiry Date':domain_expiration_date}, ignore_index=True)
			df.loc[-1]=[domain, days_to_expire, domain_expiration_date]
	df=df.reset_index()
	df['Days to expire']=df['Expiry Date'].apply(calculateDaysToExpire)
	df.to_csv('out.csv', sep='\t', encoding='utf-8',index=False, columns=['Domain','Days to expire',"Expiry Date"])
