import re
from datetime import timedelta, date
import requests
import json
import csv


states = ["Alaska","Alabama","Arkansas","American Samoa","Arizona","California","Colorado","Connecticut","District of Columbia","Delaware","Florida","Georgia","Guam","Hawaii","Iowa","Idaho","Illinois","Indiana","Kansas","Kentucky","Louisiana","Massachusetts","Maryland","Maine","Michigan","Minnesota","Missouri","Mississippi","Montana","North Carolina","North Dakota","Nebraska","New Hampshire","New Jersey","New Mexico","Nevada","New York","Ohio","Oklahoma","Oregon","Pennsylvania","Puerto Rico","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Virginia","Virgin Islands","Vermont","Washington","Wisconsin","West Virginia","Wyoming"]

states_mod = [(lambda x: re.sub("[ ,.]", "_", x))(x) for x in states]

dates = []

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

# start_dt = date(2020, 1, 24)
# end_dt = date(2020, 4, 26)


def row_date(eachState, data, eachDate):
    for eachCounty in data:
        key, value = next(iter(eachCounty.items()))
    return [eachState, key, eachDate, value['ozone']]


myFields = ['State']+dates

myFile = open('aqi.csv', 'w')
writer = csv.writer(myFile)

def getData():
	print("Fill the below Time frame:")
	start_dt = input("Enter the start date in YYYY-MM-dd format:")
	end_dt = input("Enter the end date in YYYY-MM-dd format:")
	start_dt = start_dt.split('-')
	end_dt = end_dt.split('-')
	try:
		start_dt = date(int(start_dt[0]),int(start_dt[1]),int(start_dt[2]))
		end_dt = date(int(end_dt[0]),int(end_dt[1]),int(end_dt[2]))
	except:
		print("Enter the Date in the mentioned format")
		
	for dt in daterange(start_dt, end_dt):
	    dates.append('{d.year}/{d.month}/{d.day}'.format(d=dt))

	with myFile:
	    writer.writerow(['State','County','Date','Ozone','PM 2.5','PM 10'])
	    for eachState in states_mod:
	        for eachDate in dates:
	            url = 'https://airnowgovapi.com/andata/States/'
	            my_url = url+eachState+'/'+eachDate+'.json'
	            response = requests.get(my_url,headers={})
	            try:
	                res_json = json.loads(response.json())
	                for eachCounty in res_json['reportingAreas']:
	                    key, value = next(iter(eachCounty.items()))
	                    writer.writerow([eachState, key, eachDate, value['ozone'], value['pm25'], value['pm10']])
	            except:
	                writer.writerow([eachState,'NaN','NaN','NaN','NaN','NaN'])

	print("File saved as aqi.csv")