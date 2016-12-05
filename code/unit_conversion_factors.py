
import sqlalchemy as sa
import pandas as pd
from sqlalchemy import text


conn = sa.create_engine("mysql+pymysql://CMARCINIAK:ifpri360@localhost/comtrade?charset=utf8mb4")

q = "SELECT DISTINCT commodity_code from comtradehs1997"

codes = list(pd.read_sql(q,conn)['commodity_code'])

query = """INSERT INTO conversion_factors SELECT t1.`commodity`,t1.commodity_code,t1.`reporter_code`,t2.reporter_code,t1.`trade_flow` as tf1, t2.trade_flow as tf2,t1.qty_unit, t2.qty_unit,t1.quantity as q1,t2.quantity as q2, t1.quantity/t2.quantity as ratio
FROM comtradehs1997 as t1, comtradehs1997 as t2
WHERE t1.commodity_code=%s
AND t1.commodity_code=t2.commodity_code
AND t1.reporter_code=t2.partner_code
AND t2.reporter_code=t1.partner_code
AND t1.trade_flow_code!=t2.trade_flow_code
AND t1.trade_flow_code!=3
AND t2.trade_flow_code!=3
AND t1.`qty_unit_code`=8
AND t2.`qty_unit_code`!=8""".replace("\n"," ")

#data = pd.read_sql(query,conn)
#print(data)
for code in codes:
	conn.execute(query,(code))

	
	
	
 "select commodity, AVG(kg_per_unit) from conversion_factors group by commodity"	