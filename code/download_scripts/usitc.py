import os
import requests
from bs4 import BeautifulSoup



def main():
	url = "https://www.usitc.gov/tariff_affairs/tariff_databases.htm"
	output_dir = "D:/Users/cmarciniak/Documents/macmap/data/USITC"
	res = requests.get(url)
	soup = BeautifulSoup(res.text,"html.parser")
	links = soup.find("ul",class_="rteindent1").find_all('a')
	for link in links:
		file_url = link['href']
		filename = os.path.basename(file_url)
		text = requests.get(file_url).text
		f = open(os.path.join(output_dir,filename),"w+")
		f.write(text)
		f.close()
		
if __name__ == "__main__":
	main()