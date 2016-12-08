
import sqlalchemy as sa
import pandas as pd
from sqlalchemy import text


conn = sa.create_engine("mysql+pymysql://CMARCINIAK:ifpri360@localhost/comtrade?charset=utf8mb4")

conn.execute("ALTER TABLE conversion_factors drop id")
table_list = ["comtradehs"+str(i) for i in range(1995,2015)]
table_dictionary = dict(zip(table_list,list(range(0,20))))


for table in table_list:
	table_dictionary[table] #whitelist table name
	q = "SELECT DISTINCT commodity_code from {0}".format(table)
	conn.execute("update {0} set unit_value = value/quantity where qty_unit_code=8".format(table))
	codes = list(pd.read_sql(q,conn)['commodity_code'])
	query = """INSERT INTO conversion_factors SELECT t1.`commodity`,t1.commodity_code,t1.`reporter_code`,t2.reporter_code,t1.year,t1.`trade_flow` as tf1, t2.trade_flow as tf2,t1.qty_unit, t2.qty_unit,t1.quantity as q1,t2.quantity as q2, t1.quantity/t2.quantity as ratio
	FROM {0} as t1, {0} as t2
	WHERE t1.commodity_code=%s
	AND t1.commodity_code=t2.commodity_code
	AND t1.reporter_code=t2.partner_code
	AND t2.reporter_code=t1.partner_code
	AND t1.trade_flow_code!=t2.trade_flow_code
	AND t1.trade_flow_code!=3
	AND t2.trade_flow_code!=3
	AND t1.`qty_unit_code`=8
	AND t2.`qty_unit_code`!=8""".replace("\n"," ").replace("\t"," ").format(table)
	for code in codes:
		conn.execute(query,(code))

	
	
	
