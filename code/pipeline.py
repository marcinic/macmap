

import dask
from dask.dot import dot_graph
from download_scripts import comtrade, unctad_specific, unctad_advalorem, usitc

dsk = {
	'download-comtrade': (comtrade.main),
	'download-unctad-specific': (unctad_specific.main),
	'download-unctad-advalorem': (unctad_advalorem.main),
	'download-usitc': (usitc.main)
}

dot_graph(dsk)