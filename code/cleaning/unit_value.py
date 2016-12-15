
import sqlalchemy as sa
import pandas as pd
from sqlalchemy import Table,bindparam, and_, text
from sqlalchemy.ext.declarative import declarative_base

conn = sa.create_engine("mysql+pymysql://CMARCINIAK:ifpri360@localhost/comtrade?charset=utf8mb4")


#conn.execute("ALTER TABLE conversion_factors drop id")
table_list = ["comtradehs"+str(i) for i in range(1995,2015)]
table_dictionary = dict(zip(table_list,list(range(0,20))))


def unit_values(table,engine):
	engine.execute("update {0} set unit_value = value/quantity where qty_unit_code=8".format(table))
	engine.execute("update {0} set unit_value = value/netweight_kg where qty_unit_code!=8 and netweight_kg!=0 and netweight_kg is not null".format(table))

def conversion_factors(table,engine):
	table_dictionary[table] 
	q = "SELECT DISTINCT commodity_code from {0}".format(table)
	codes = list(pd.read_sql(q,conn)['commodity_code'])
	query = """INSERT INTO conversion_factors SELECT t1.`commodity`,t1.commodity_code,t1.`reporter_code`,t2.reporter_code,t1.year,t1.classification,t1.`trade_flow` as tf1, t2.trade_flow as tf2,t1.qty_unit, t2.qty_unit,t1.quantity as q1,t2.quantity as q2, t1.quantity/t2.quantity as ratio
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
		engine.execute(query,(code))

def compute_average_weight(table,engine):
	query = """UPDATE {0}, 
	(select commodity_code,classification, AVG(kg_per_unit) as avg_kg from conversion_factors group by commodity_code,classification) as akg
	set est_kg = avg_kg
	where {0}.commodity_code=akg.commodity_code
	AND {0}.classification = akg.classification
	AND {0}.qty_unit_code!=8""".replace("\n"," ").replace("\t"," ").format(table)
	engine.execute(query)
	engine.execute("update {0} set unit_value = value/(quantity*est_kg) where unit_value is null and quantity is not null".format(table))

def compute_median_weight(tablename,engine):
	q = "select commodity,commodity_code,kg_per_unit from conversion_factors"
	data = pd.read_sql(q,engine)
	med = data.groupby("commodity_code").median()
	med['commodity_code'] = med.index
	med_values = list(med.T.to_dict().values())
	
	Base = declarative_base()
	table = Table(tablename,Base.metadata,autoload=True,autoload_with=engine)
	
	stmt = table.update()\
	.where(
    and_(table.c.commodity_code==bindparam("commodity_code"),
         table.c.unit_value==None))\
	.values({'commodity_code':bindparam('commodity_code'),
        'est_kg': bindparam('kg_per_unit')
        })

	conn.execute(stmt,med_values)
	
	engine.execute("update {0} set unit_value = value/(quantity*est_kg) where unit_value is null and quantity is not null".format(tablename))
	
	
def calculate_unit_values():
	for table in table_list:
		unit_values(table,conn)
		conversion_factors(table,conn)
		compute_median_weight(table,conn)
		
if __name__=="__main__":
	table = "comtradehs1997"
	unit_values(table,conn)
	conversion_factors(table,conn)
	compute_median_weight(table,conn)
	
