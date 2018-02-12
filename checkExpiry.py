#!/usr/bin/python3

import whois
from datetime import datetime
from sys import argv,exit
import pandas as pd
import numpy as np
import os.path

def calculateDaysToExpire(ExpiryDate):
	print (ExpiryDate)
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

	for domain in content:
		if (domain not in df.index) or np.isnan(df.at[domain,'Days to expire']):
		#if (domain not in df.index):
			try:
				w = whois.whois(domain)

				if (w.expiration_date and w.status) == None:
					days_to_expire=999
					domain_expiration_date=999

				if type(w.expiration_date) == list:
					w.expiration_date = w.expiration_date[0]
					timedelta = w.expiration_date - now
					days_to_expire = timedelta.days
				else:
					domain_expiration_date = str(w.expiration_date.day) + '/' + str(w.expiration_date.month) + '/' + str(w.expiration_date.year)
				timedelta = w.expiration_date - now
				days_to_expire = timedelta.days

			except (whois.parser.PywhoisError):
					days_to_expire=999
					domain_expiration_date=999
                    
			#df=df.append({'Domain':domain, 'Days to expire':days_to_expire, 'Expiry Date':domain_expiration_date},ignore_index=True)
			df=df.append({'Domain':domain, 'Days to expire':days_to_expire, 'Expiry Date':domain_expiration_date}, ignore_index=True)
			#df['Days to expire'].replace(999,np.nan)
			#df['Expiry Date'].replace(999,np.nan)
			df.replace(int('999'),np.nan)
			df.replace(int('999'),np.nan)
		else:
			df['Days to expire']=df['Expiry Date'].apply(calculateDaysToExpire)
		#df.to_csv('out.csv', sep='\t', encoding='utf-8', index_label='Domain')
	df.to_csv('out.csv', sep='\t', encoding='utf-8',index=False,columns=['Domain','Days to expire',"Expiry Date"])



