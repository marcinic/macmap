
import sqlalchemy as sa
from sqlalchemy import Column,Index,Float, Integer, String,Text
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
conn = sa.create_engine("mysql+pymysql://CMARCINIAK:ifpri360@localhost/comtrade?charset=utf8mb4")

def create_comtrade(tablename):
	class Comtrade(Base):
		__tablename__ = tablename
		__table_args__ = (
			Column('id',Integer,primary_key=True),
			Column('classification',String(4)),
			Column('year',Integer),
			Column('period',String(10)),
			Column('aggregate_level',Integer),
			Column('is_leaf_code',Integer),
			Column('trade_flow_code',Integer),
			Column('trade_flow',String(255)),
			Column('commodity_code',mysql.VARCHAR(6)),
			Column('commodity',Text),
			Column('reporter_code',Integer),
			Column('reporter',String(255)),
			Column('reporter_iso',String(3)),
			Column('partner_code',Integer),
			Column('partner_iso',String(3)),
			Column('partner',String(255)),
			Column('qty_unit_code',Integer),
			Column('qty_unit',String(255)),
			Column('flag',Integer),
			Column('netweight_kg',Float),
			Column('quantity',Float),
			Column('value',Float),
			Column('unit_value',Float),
			Column('kg_conversion_factor',Float),
			Column('H3_commodity_code',mysql.VARCHAR(6)),
			Index('commodity_index','commodity_code','reporter_code')
		)
	return Comtrade

	
	
def create_mirrorflow(tablename):
		class MirrorFlow(Base):
			__tablename__ = tablename
			__table_args__ = (
				Column('id',Integer,primary_key=True),
				Column('id_m',Integer),
				Column('id_x',Integer),
				Column('reporter_iso_m',String(3)),
				Column('parnter_iso_m',String(3)),
				Column('reporter_iso_x',String(3)),
				Column('parnter_iso_x',String(3)),
				Column('commodity_code',mysql.VARCHAR(6)),
				Column('classification_m',String(4)),
				Column('classification_x',String(4)),
				Column('value_x',Float),
				Column('value_m',Float),
				Column('netweight_kg_x',Float),
				Column('netweight_kg_m',Float),
				Column('unit_value_x',Float),
				Column('unit_value_m',Float),
			)
	
class ConversionFactors(Base):
	
	def ratio(context):
		return context.current_parameters['quantity1']/context.current_parameters['quantity2']
	
	__tablename__ = "conversion_factors"
	
	__table_args__ = (
		Column('id',Integer,primary_key=True),
		Column('commodity',Text),
		Column('commodity_code',mysql.VARCHAR(6)),
		Column('reporter_code',Integer),
		Column('partner_code',Integer),
		Column('year',Integer),
		Column('classification',String(4)),
		Column('trade_flow1',String(255)),
		Column('trade_flow2',String(255)),
		Column('quantity_unit1',String(255)),
		Column('quantity_unit2',String(255)),
		Column('quantity1',Float),
		Column('quantity2',Float),
		Column('kg_per_unit',Float, default=ratio)
	)


def whitelist(tablename,table_list):
	table_dictionary = dict(zip(table_list,list(range(0,20))))
	return table_dictionary[tablename]

def drop_index(tablename,table_list,engine):
	try:
		whitelist(tablename,table_list)
		query1 = "ALTER TABLE {0} MODIFY id INT".format(tablename)
		query2 = "ALTER TABLE {0} DROP PRIMARY KEY".format(tablename)
		engine.execute(query1)
		engine.execute(query2)
		engine.execute(query1)
		
	except KeyError:
		print("table name "+tablename+" is not valid")


		
def main():
	table_list = ["comtradehs"+str(i) for i in range(1995,2016)]
	create_mirrorflow("mirrorflow1996")
	for table in table_list:
		create_comtrade(table)
	Base.metadata.create_all(conn)
	#drop_index("conversion_factors",["conversion_factors"],conn)
	#conn.execute("ALTER TABLE conversion_factors DROP id")
	#table_list.append("conversion_factors")

		
if __name__=="__main__":	
	main()