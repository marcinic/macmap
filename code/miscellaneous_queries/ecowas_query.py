

import sqlalchemy as sa
import pandas as pd


conn = sa.create_engine("mysql+pymysql://CMARCINIAK:ifpri360@localhost/comtrade?charset=utf8mb4")


reporter_isos = ["'MAR'","'BEN'","'BFA'","'CIV'","'GHA'","'GIN'","'GNB'","'GMB'","'MLI'","'NER'","'NGA'","'SEN'","'SLE'","'TGO'"]

def query_country(iso3):
    country_15 = pd.read_sql("SELECT value,commodity_code,commodity,year,reporter_iso from comtradehs2015 where trade_flow_code=1 and reporter_iso={}".format(iso3),conn)
    country_16 = pd.read_sql("SELECT value,commodity_code,commodity,year,reporter_iso from comtradehs2016 where trade_flow_code=1 and reporter_iso={}".format(iso3),conn)
    return pd.concat([country_15,country_16])

data = pd.DataFrame()
"""for iso in reporter_isos:
    print("Querying "+iso)
    d = query_country(iso)
    d = d.groupby(['commodity_code','year'],as_index=False).value.sum()
    data = pd.concat([data,d])
"""


('MAR','BEN','BFA','CIV','GHA','GIN','GNB','GMB','MLI','NER','NGA','SEN','SLE','TGO')


country_15 = pd.read_sql("SELECT value,commodity_code,commodity,year,partner_iso,reporter_iso from comtradehs2015 where trade_flow_code=1 and reporter_iso IN ('MAR','BEN','BFA','CIV','GHA','GIN','GNB','GMB','MLI','NER','NGA','SEN','SLE','TGO')",conn)
country_16 = pd.read_sql("SELECT value,commodity_code,commodity,year,partner_iso,reporter_iso from comtradehs2014 where trade_flow_code=1 and reporter_iso IN ('MAR','BEN','BFA','CIV','GHA','GIN','GNB','GMB','MLI','NER','NGA','SEN','SLE','TGO')",conn)
data = pd.concat([country_15,country_16])
#data = data.groupby(['commodity_code','commodity','reporter_iso','year'],as_index=False).value.sum()

data.to_csv("C:\\Users\\CMARCINIAK\\Documents\\macmap\\ecowas_14_15.csv")
