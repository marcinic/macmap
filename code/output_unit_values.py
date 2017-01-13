
import sqlalchemy as sa

# script to dump database as csv


table_list = ["comtradehs"+str(i) for i in range(2012,2015)]

conn = sa.create_engine("mysql+pymysql://CMARCINIAK:ifpri360@localhost/comtrade?charset=utf8mb4")
query = """select classification,year,trade_flow,commodity_code,commodity,reporter_code,reporter,reporter_iso,partner_code,partner_iso,partner,qty_unit,qty_unit_code,flag,netweight_kg,quantity,value,unit_value,kg_conversion_factor from {0} INTO OUTFILE '{0}.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"';
"""

for table in table_list:
	conn.execute(query.format(table))
