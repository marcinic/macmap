
import os
import time
import math
import pandas as pd
import numpy as np
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func, select,insert, between, Table


data_dir = "D:/Users/cmarciniak/Documents/macmap/data"
file = os.path.join(data_dir,"dist_cepii.csv")
distances = pd.read_csv(file)
country_file = os.path.join(data_dir,"geo_cepii.xls")
geo_cepii = pd.read_excel(country_file,"geo_cepii")

conn = sa.create_engine("mysql+pymysql://CMARCINIAK:ifpri360@localhost/comtrade?charset=utf8mb4")


Base = declarative_base()
table = Table("comtradehs1997",Base.metadata,autoload=True,autoload_with=conn)
mf_table = Table("mirrorflow1997",Base.metadata,autoload=True,autoload_with=conn)


def row_count(table):
	stmt = select([func.count()]).select_from(table)
	res = conn.execute(stmt)
	count = list(res)[0][0]
	return count

def chunk(num_rows):
	"""
		Divides the database rows into chunks that can fit into memory
	"""
	i = 1
	chunks = []
	while i < num_rows:
		chunks.append(i)
		i = i+1000000
		if i>num_rows:
			chunks.append(num_rows)
	return chunks

	
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]	
	

def select_trade_flow(table,trade_flow_code):
	""" Returns SQLAlchemy statement for trade flows of a given type"""
	stmt = select([table.c.id,
	table.c.commodity_code,
	table.c.reporter_iso,
	table.c.partner_iso,
	table.c.classification,
	table.c.value,
	table.c.netweight_kg,
	table.c.unit_value]).where(table.c.trade_flow_code==trade_flow_code)
	return stmt
	

def remaining_rows():
	import_rows = pd.read_sql("select id_m from mirrorflow1997",conn)
	export_rows = pd.read_sql("select id_x from mirrorflow1997",conn)


	im_rows = np.array(import_rows['id_m'].dropna(),dtype="int64")
	ex_rows = np.array(export_rows['id_x'].dropna())
	rows = np.append(im_rows,ex_rows)


	ids = [i for i in range(1,7581114)]
	id_dictionary = {el:0 for el in ids}
	for row in rows:
		if row in id_dictionary:
			id_dictionary.pop(row,None)

	remaining_rows = tuple(id_dictionary.keys())
	return remaining_rows
	
def insert_import_rows(remaining_rows):
	print("inserting_rows")
	select_query = select( [table.c.id,
			table.c.commodity_code,
			table.c.reporter_iso,
			table.c.partner_iso,
			table.c.classification,
			table.c.value,
			table.c.netweight_kg,
			table.c.unit_value],table.c.id.in_(remaining_rows))

	insert_query = insert(mf_table).from_select( 
		(mf_table.c.id_m,
		mf_table.c.commodity_code,
		mf_table.c.reporter_iso_m,
		mf_table.c.partner_iso_m,
		mf_table.c.classification_m,
		mf_table.c.value_m,
		mf_table.c.netweight_kg_m,
		mf_table.c.unit_value_m
		),select_query
	)
	
	conn.execute(insert_query)

	
	
	
	
def mirror_flow(tablename):
	""" 
		Iterate through the exports in a table. 
		Merge with imports and write to MySQL 
	"""
	Base = declarative_base()
	table = Table(tablename,Base.metadata,autoload=True,autoload_with=conn)
	
	select([func.count()]).select_from(table)
	
	print("importing imports")
	import_query = select_trade_flow(table,1)
	imports = pd.read_sql(import_query,conn)
	
	
	
	table_length = row_count(table)
	chunks = chunk(table_length)
	
	
	export_query = select_trade_flow(table,2)
	i = 0
	while i < len(chunks)-1:
		print("querying chunk {0}, {1}".format(chunks[i],chunks[i+1]))
		exp_q = export_query.where(between(table.c.id,chunks[i]+1,chunks[i+1]))
		exports = pd.read_sql(exp_q,conn)
		print("merging")
		m = imports.merge(exports, 
			how='right',
			left_on=['commodity_code','partner_iso','reporter_iso'],
			right_on=['commodity_code','reporter_iso','partner_iso'], 
			suffixes=('_m','_x'))
		print("inserting into database")
		m.to_sql("mirrorflow1998",conn,if_exists="append",index=False)
		i = i+1
		
		
		
if __name__=="__main__":
	start = time.time()
	rows = remaining_rows()
	row = chunks(rows,100000)
	for r in row:
		insert_import_rows(tuple(r))
	#print(len(rows))
	#insert_import_rows(rows[0:1000])	
	end = time.time()
	print(str(end-start)+" seconds")
		




