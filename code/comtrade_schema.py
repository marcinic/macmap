
import sqlalchemy as sa
from sqlalchemy import Column,Float, Integer, String
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
conn = sa.create_engine("mysql+pymysql://CMARCINIAK:ifpri360@localhost/comtrade?charset=utf8mb4")

class Comtrade(Base):
	__tablename__ = "comtradehs1999"
	__table_args__ = (
		Column('id',Integer,primary_key=True),
		Column('classification',String(4)),
		Column('year',Integer),
		Column('period',String(10)),
		Column('aggregate_level',Integer),
		Column('is_leaf_code',Integer),
		Column('trade_flow_code',Integer),
		Column('trade_flow',String(255)),
		Column('reporter_code',Integer),
		Column('reporter',String(255)),
		Column('reporter_iso',String(3)),
		Column('partner_code',Integer),
		Column('partner_iso',String(3)),
		Column('partner',String(255)),
		Column('qty_unit_code',Integer),
		Column('qty_unit',String(255)),
		Column('commodity_code',mysql.VARCHAR(6)),
		Column('commodity',String(255)),
		Column('flag',Integer),
		Column('netweight_kg',Float),
		Column('quantity',Float),
		Column('value',Float),

	)
	
class ConversionFactors(Base):
	
	def ratio(context):
		return context.current_parameters['quantity1']/context.current_parameters['quantity2']
	
	__tablename__ = "conversion_factors"
	
	__table_args__ = (
		Column('id',Integer,primary_key=True),
		Column('commodity',String(255)),
		Column('commodity_code',mysql.VARCHAR(6)),
		Column('reporter_code',Integer),
		Column('partner_code',Integer),
		Column('trade_flow1',String(255)),
		Column('trade_flow2',String(255)),
		Column('quantity_unit1',String(255)),
		Column('quantity_unit2',String(255)),
		Column('quantity1',Float),
		Column('quantity2',Float),
		Column('kg_per_unit',Float, default=ratio)		
	)


	
Base.metadata.create_all(conn)