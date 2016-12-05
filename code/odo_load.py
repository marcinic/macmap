import pandas as pd
import os
from odo import odo
from datashape import Categorical

data_dir = "D:/Users/cmarciniak/Documents/macmap/data/comtrade"
file = "comtradeHS1995.zip"
data = os.path.join(data_dir,file)
chunk_size=10**6
fn = lambda x: x.lower().replace(" ","_").replace("$","").replace("(","").replace(")","")



reader = pd.read_table(data,sep=",",dtype="object",chunksize=chunk_size)
chunk = reader.get_chunk(chunk_size)

chunk = chunk[chunk.Partner!="World"]
chunk = chunk[chunk['Commodity Code']!='TOTAL'] # remove totals
#chunk['reporter_code'] = chunk['Reporter Code'].astype(int)
chunk['quantity'] = chunk.Qty.astype(float)
chunk['value'] = chunk['Trade Value (US$)'].astype(float)
chunk = chunk[chunk.quantity!=0] # remove zero trade flows
chunk['Commodity Code'] = chunk['Commodity Code'].map(lambda x: x.encode('ascii','ignore'))
chunk['Partner'] = chunk['Partner'].str.encode('ascii','ignore')

col = list(map(fn,chunk.columns))
chunk.columns = col 
chunk.drop('trade_value_us',axis=1,inplace=True)
chunk.drop('qty',axis=1,inplace=True)

categorical = type(pd.Categorical.dtype)
for k in chunk.columns:
    print(k+" "+str(isinstance(chunk[k].dtype,categorical)))

chunk = chunk.astype(object).where(pd.notnull(chunk), None)		
odo(chunk,"mysql+pymysql://CMARCINIAK:ifpri360@localhost/comtrade::test")