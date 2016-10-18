
import os
import requests
import logging
import pandas as pd
import xml.etree.ElementTree as ET


def get_country_codes():
	"""
		Returns list of all available country codes from WITS, excluding regional trade agreements. 
	"""
	countries_url = "http://wits.worldbank.org/API/V1/wits/datasource/trn/country/ALL"
	res = requests.get(countries_url)
	root = ET.fromstring(res.text[3::]) # xml not well formed, contains extra charachters
	countries = root.findall(".//{http://wits.worldbank.org}country")
	codes = [country.attrib['countrycode'] for country in countries]
	country_codes = [x for x in codes if x.isdigit()] # filters regional trade agreement codes
	return country_codes

def make_url(reporter,partner,year):
	"""
		Returns url string with reporter, partner and year parameters
	"""
	url = "http://wits.worldbank.org/API/V1/SDMX/V21/datasource/TRN/reporter/{}/partner/{}/product/ALL/year/{}/datatype/reported".format(reporter,partner,year)
	return url

	
def get_available():
	"""
		Returns list of country code, year pairs from the available data
	"""
	data_availability = "http://wits.worldbank.org/API/V1/wits/datasource/trn/dataavailability/"
	res = requests.get(data_availability)
	root = ET.fromstring(res.text[3::])
	reporters = root.findall(".//{http://wits.worldbank.org}reporter")
	pairs = []
	for reporter in reporters:
		name = reporter.attrib['countrycode']
		year = reporter.find("{http://wits.worldbank.org}year").text
		partner_list = reporter.find("{http://wits.worldbank.org}partnerlist").text.split(";")
		partner_list.pop()
		pairs.append((name,year,partner_list))	
	return pairs
	

def get_urls():
	"""
		Returns list of all urls to be queried
	"""
	available_data = get_available()
	urls = []
	for row in available_data:
		for partner in row[2]:
			filename = row[0]+"_"+partner+"_"+row[1]+".csv"
			url = make_url(row[0],partner,row[1])
			urls.append((filename,url))
	return urls
	
def parse_response(res):
	"""
		Returns list of dictionaries where each dictionary is an instance from an API call.
	"""
	tree = ET.fromstring(res.content)
	series = tree.findall(".//Series")
	rows = []
	for s in series:
		observation = s.find("./Obs")
		row = {**s.attrib,**observation.attrib}
		rows.append(row)
	return rows
	
def output_file(filename,rows,output_dir):
	"""
		Writes data rows to a csv file
	"""
	data = pd.DataFrame(rows)
	outfile = os.path.join(output_dir,filename)
	data.to_csv(outfile)
	
def main():
	urls = get_urls()
	output_dir = "D:/Users/cmarciniak/Documents/macmap/data/unctad/advalorem"
	for url in urls:
		res = requests.get(url[1])
		rows = parse_response(res)
		output_file(url[0],rows,output_dir)
		
		
if __name__=="__main__":
	main()