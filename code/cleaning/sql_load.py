
import os
import re
import time
import multiprocessing
import traceback
import pandas as pd
import numpy as np
import sqlalchemy as sa
from odo import odo
from multiprocessing import Pool
from sqlalchemy.sql import text
#from nomenclature_conversion import convert


data_dir =  "D:/Users/cmarciniak/Documents/macmap/data/comtrade"


def init_db():
	engine = sa.create_engine("mysql+pymysql://root@localhost")
	engine.execute("CREATE DATABASE comtrade")
	engine.execute("ALTER DATABASE comtrade CHARACTER SET utf8 COLLATE utf8_unicode_ci")

	
def get_inputs(data_dir):
	files = os.listdir(data_dir)
	zipfiles = [os.path.join(data_dir,f) for f in files if f.endswith(".zip")]
	return zipfiles

def get_table_name(filename):
	return os.path.splitext(os.path.basename(filename))[0].lower()
	
def load_to_sql(file):
	try:
		table_name = get_table_name(file)
		tn = {"table_name":table_name,"index":"ix_"+table_name+"_index"}
		chunk_size=1500000
		fn = lambda x: x.lower().replace(" ","_").replace("$","").replace("(","").replace(")","")
		reader = pd.read_table(file,sep=',',dtype="object",chunksize=chunk_size,encoding='utf-8')
		conn = sa.create_engine("mysql+pymysql://CMARCINIAK:ifpri360@localhost/comtrade?charset=utf8mb4")
		
		for chunk in reader:
			chunk = chunk[chunk.Partner!="World"]
			chunk = chunk[chunk['Commodity Code']!='TOTAL'] # remove totals
			chunk = chunk[chunk['Aggregate Level']=='6'] # remove subtotals
			chunk['reporter_code'] = chunk['Reporter Code'].astype(int)
			chunk['quantity'] = chunk.Qty.astype(float)
			chunk['value'] = chunk['Trade Value (US$)'].astype(float)
			chunk = chunk[chunk.quantity!=0] # remove zero trade flows

						
			col = list(map(fn,chunk.columns))
			chunk.columns = col 
			
			
			chunk.drop('trade_value_us',axis=1,inplace=True)
			chunk.drop('qty',axis=1,inplace=True)
			chunk.drop('period_desc.',axis=1,inplace=True)
			
			#chunk['H3_commodity_code'] = convert(chunk)
			
			chunk = chunk.astype(object).where(pd.notnull(chunk), None)		
			#odo(chunk,"mysql+pymysql://CMARCINIAK:ifpri360@localhost/comtrade::"+table_name )
			chunk.to_sql(name=table_name,if_exists='append',con=conn,index=False)
		
	except UnicodeEncodeError:
		print("Unicode error at "+table_name)
		traceback.print_exc()
		
def comtrade_data():
	inputs = get_inputs(data_dir)
	for input in inputs:
		load_to_sql(input)
"""
conn.execute(text("ALTER TABLE DROP INDEX first from cmtrd95"))	
conn.execute(text("ALTER TABLE cmtrd95 MODIFY `reporter_code` INTEGER")) # maybe faster to modify them before insert
conn.execute(text("ALTER TABLE cmtrd95 MODIFY `partner_code` INTEGER"))	
conn.execute(text("ALTER TABLE cmtrd95 change `commodity_code` `commodity_code` VARCHAR(6)"))
conn.execute(text("ALTER TABLE cmtrd95 PARTITION BY KEY(commodity_code)"),)
"""
if __name__=="__main__":
	start = time.time()
	#threads = multiprocessing.cpu_count()
	inputs = get_inputs(data_dir)
	for input in inputs:
		load_to_sql(input)
	#load_to_sql(inputs[2])
	#load_to_sql(inputs[0])
	#p = Pool(threads)
	#p.map(load_to_sql,inputs)
	end = time.time()
	print(str((end-start)/60)+" minutes elapsed")