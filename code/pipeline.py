

import dask
from dask.dot import dot_graph
from download_scripts import comtrade, unctad_specific, unctad_advalorem, usitc
from cleaning import sql_load, comtrade_schema, unit_value

dsk = {
	'download-comtrade': (comtrade.main),
	'download-unctad-specific': (unctad_specific.main),
	'download-unctad-advalorem': (unctad_advalorem.main),
	'download-usitc': (usitc.main),
	'comtrade-schema':(comtrade_schema.main),
	'load-comtrade':(sql_load.comtrade_data,['comtrade-schema']),
	'unit-values':(unit_value.calculate_unit_values,['load-comtrade'])
}

dot_graph(dsk)

#dask.get(dsk,['comtrade-schema','load-comtrade','unit_values'])