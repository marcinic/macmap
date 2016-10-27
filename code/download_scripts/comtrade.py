
import os
import io
import zipfile
import requests



def make_url(type,freq,period,reporter,classification,token):
	"""
		Returns url string for a set of parameters
		
		type: C for commodities or S for Services
		freq: A for annual or M for monthly
		period: year or date code in the format yyyy or yyyymm
		reporter: 3-digit reporter code or ALL for all countries
		classification: nomenclature code for products 
		Parameters can be found at http://comtrade.un.org/data/doc/api/bulk/
	"""
	return "http://comtrade.un.org/api/get/bulk/{}/{}/{}/{}/{}?token={}".format(type,freq,period,reporter,classification,token)

	
def output_file(filename,res,output_dir):
	"""
		Writes the response from bulk API request to zip file.
	"""
	outfile = os.path.join(output_dir,filename)
	f = open(outfile,"wb")
	f.write(res.content)
	f.close()


def main():
	output_dir = "D:/Users/cmarciniak/Documents/macmap/data/comtrade"
	f = open("comtrade_token.txt")
	token = f.read()
	#years = [str(year) for year in range(1995,2015)]
	years = ["2015"]
	for year in years:
		url = make_url("C","A",year,"ALL","HS",token)
		res = requests.get(url)
		output_file("comtradeHS"+year+".zip",res,output_dir)




if __name__=="__main__":
	main()
