import pandas as pd
import sqlalchemy as sa

conn = sa.create_engine("mysql+pymysql://CMARCINIAK:ifpri360@localhost/comtrade?charset=utf8mb4")


def make_query(number):
    query = "SELECT classification,year,commodity_code,partner_iso,reporter_iso,value,quantity,netweight_kg,kg_conversion_factor,qty_unit,trade_flow FROM comtradehs2013 where trade_flow_code < 3 and commodity_code like '{0}%%';"
    return query.format(str(number))

	
	
def query_year():
	"""Query a years worth of data """
	chapters = [0,1,20,21,22,23,24,50,51]
	
	queries = list(map(make_query,chapters))
	data = pd.DataFrame()
	for query in queries:
		table = pd.read_sql(query,conn)
		data = pd.concat([data,table])
	data['HS4'] = data.commodity_code.map(lambda x: x[0:4])
	data.netweight_kg = data.netweight_kg.fillna(0)
	agg = data.groupby(["HS4","reporter_iso","partner_iso","trade_flow","year"],as_index=False).sum()
	#output = agg[['value','quantity','netweight_kg']]

	agg.to_csv("output_2013b.csv")
	
	
	
query_year()