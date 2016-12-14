
import os
import pandas as pd


data_dir = "D:/Users/cmarciniak/Documents/macmap/data/nomenclature"


def create_nomenclature_dictionary(file,nomenclature,input_header):
	data = pd.read_csv(file,dtype="object",encoding="latin1")
	df = pd.DataFrame()
	df['H3'] = data['HS 2007 Product Code']
	df[nomenclature] = data[input_header]
	conversion = df.set_index(nomenclature)['H3'].to_dict()
	return conversion
	
	
def conversion_table():
	file = os.path.join(data_dir,"Concordance_H3_to_H0/JobID-44_Concordance_H3_to_H0.csv")	
	file1 = os.path.join(data_dir,"Concordance_H3_to_H1/JobID-45_Concordance_H3_to_H1.csv")
	file2 = os.path.join(data_dir,"Concordance_H3_to_H2/JobID-46_Concordance_H3_to_H2.csv")

	h0_conversion = create_nomenclature_dictionary(file,"H0",'HS 1988/92 Product Code')
	h1_conversion = create_nomenclature_dictionary(file1,"H1","HS 1996 Product Code")	 
	h2_conversion = create_nomenclature_dictionary(file2,"H2","HS 2002 Product Code")
	conversion = {"H0":h0_conversion,"H1":h1_conversion,"H2":h2_conversion}
	return conversion
	

def convert(df):
	conv = conversion_table()
	a = df[df.classification=="H0"].commodity_code.map(conv["H0"])
	b = df[df.classification=="H1"].commodity_code.map(conv["H1"])
	c = df[df.classification=="H2"].commodity_code.map(conv["H2"])
	return pd.concat([a,b,c])
	
	

