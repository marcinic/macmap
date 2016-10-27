import os
import re
import traceback
import requests
import pandas as pd
from bs4 import BeautifulSoup


def prepare_url(iso3_code,year):	
	""" 
		Returns url string for UNCTAD graphical interface

	"""
	page_size = get_page_size(iso3_code,year)
	url = "http://wits.worldbank.org/tariff/trains/en/country/{}/year/{}/pagenumber/1/pageSize/{}".format(iso3_code,str(year),page_size)
	return url
	
	
def get(url):
	"""
		Returns a list of rows formatted as dictionaries from UNCTAD interface
	"""
	rows = []
	try:
		page_size = get_page_size(url)
		url = url.replace("100",page_size)
		res = requests.get(url)
		
		soup = BeautifulSoup(res.text,"html.parser")
		scripts = soup.find_all("script")
		p = re.search("(localdata: \[)(.*)",scripts[7].text)
		data = p.group(2)
		
		row_strings = [s+"," for s in data.split("},")]
		rows = parse_row_strings(row_strings)
	except IndexError:
		traceback.print_exc()
	except AttributeError:
		traceback.print_exc()
	return rows

def get_available_data():
	"""
		Returns list of urls for available data from the interface
	"""
	url = "http://wits.worldbank.org/tariff_dataavailability.aspx?lang=en"
	res = requests.get(url)
	soup = BeautifulSoup(res.text,"html.parser")
	table = soup.find("div",class_="content").find_all("table")[1]
	elements = table.find_all("td")
	links = [element.find("a") for element in elements]
	links = list(filter(lambda x:x!=None,links))
	urls = [link['href'] for link in links]
	return urls
	
def parse_row_strings(row_strings):
	"""
		Returns a list of dictionaries from string of javscript object
	"""
	fields = ['ProductCode','ProductDescription','Partner',
			'PartnerName','AdValorem','MeasureName',
			'NonAdValorem','AffectedPartners']
	output = []
	for row in row_strings:
		r = {}
		for f in fields:
			s = re.search("(?<="+f+" :)(.*?)(?=,)",row)
			value = s.group(0).replace("\"","").replace("}\r","")
			r.update({f:value})
		output.append(r)
	return output
	
def get_page_size(url):
	"""
		Returns the number of available records for a country and year
	"""
	page_size = "200000"
	res = requests.get(url)
	soup = BeautifulSoup(res.text,"html.parser")
	scripts = soup.find_all("script")
	p = re.search('var totalRecords= ([0-9]{1,6})',scripts[7].text)
	try:
		page_size = p.group(1)
	except AttributeError:
		traceback.print_exc()
	return page_size

def main(urls,output_dir):	
	output_dir = "D:/Users/cmarciniak/Documents/macmap/data/unctad/specific/"
	for url in urls:
		print(url)
		iso3_code = re.search("[A-Z]{3}",url).group(0)
		year = re.search("[0-9]{4}",url).group(0)
		res = get(url)
		if(res==[]):
			print("No data found at "+url)
		else:
			data = pd.DataFrame(res)
			data['Year'] = year
			data['ISO3Code'] = iso3_code
			out_file = os.path.join(output_dir,iso3_code+year+".csv")
			data.to_csv(out_file)
			
if __name__=="__main__":
	output_dir = "D:/Users/cmarciniak/Documents/macmap/data/unctad/specific/"
	urls = get_available_data()
	main(urls,output_dir)
		