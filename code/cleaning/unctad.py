
import os
from bs4 import BeautifulSoup
import pandas as pd
from pandas.parser import CParserError


currency_codes = {
    	'F': 'Aruban Florin',
        'AMD':'Armenian Dram',
    	'BD': 'Local Currency',
    	'DH':'Arab Emirates Dirham',
    	'AED':'Arab Emirates Dirham',
    	'DLARES':'USD',
    	'$':'USD',
    	'USD':'USD',
    	'EUR':'Euro',
        'EURO':'Euro',
        'BHD':'Bahraini Dinar',
    	'BSD':'Bahamian Dollar',
    	'KM':'Bosnian Mark',
    	'BZD':'Belize Dollar',
    	'BMD':'Bermudan Dollar',
    	'Bolivian':'Bolivian Boliviano',
    	'C':'cents',
    	'CENTS':'cents',
    	'CFA':'Central African Franc',
    	'FR.':'Local Franc',
    	'SFR':'Swiss Franc',
    	'RMB':'Chinese Yuan',
    	'YUAN':'Chinese Yuan',
    	'CNY':'Chinese Yuan',
    	'NZD':'New Zealand Dollar',
    	'CYP':'Cypriot Pound',
    	'C£':'Cypriot Pound',
    	'DA':'Algerian Dinar',
        'DR':'Dominican Peso',
    	'EGP':'Egyptian Pound',
    	'POUND':'Local Pound',
    	'LE':'Egyptian Pound',
    	'EGL':'Egyptian Pound',
    	'ECU':'European Currency Unit',
    	'FJD':'Fijian Dollar',
    	'GMD':'Gambian Dalasi',
    	'RS':'Local Rupee',
    	'ISK':'Iceland Krona',
    	'SDR':'Special Drawing Right',
    	'KR':'Swedish Kroner',
    	'NIS':'Israeli New Sheqel',
    	'YEN':'Japanese Yen',
    	'Y':'Japanese Yen',
    	'KES':'Kenyan Shilling',
    	'SHS.':'Kenyan Shilling',
        'SH':'Shilling',
    	'XCD':'East Caribbean Dollar',
    	'WON':'Korean Won',
    	'LYH':'Libyan Dinar',
    	'LYD':'Libyan Dinar',
    	'DINAR':'Libyan Dinar',
    	'S':'Peruvian Sole',
    	'RM':'Malaysian Ringgit',
    	'M$':'Malaysian Ringgit',
    	'NGN':'Nigerian Naira',
    	'NK':'Norwegian Kroner',
    	'NOK':'Norwegian Kroner',
    	'KRONE':'Norwegian Kroner',
    	'BALBOA':'Panamanian Balboa',
    	'SAR':'Saudi Riyal',
    	'SR':'Saudi Riyal',
    	'SGD':'Singaporean Dollar',
    	'S$':'Singaporean Dollar',
    	'SBD':'Solomon Island Dollar',
    	'SIT':'Slovenian Tolar',
    	'SR':'Saudi Riyal',
    	'BHT':'Thai Baht',
    	'BAHTS':'Thai Baht',
    	'B':'Thai Baht',
    	'AUD':'Australian Dollar',
        'A$':'Australian Dollar',
    	'NT$':'New Taiwan Dollar',
    	"BOLIVARES":"Bolivian Bolivar",
    	"SAT$":"Samoan Tala",
    	"ZAR":"South African Rand",
    	"RAND":"South African Rand"
    }
units = {
    'KILOGRAMO':'kg',
	'KG':'kg',
	'LI':'litre',
	'LITRE':'liter',
    'LITER':'liter',
	'DOZEN': 'dozen',
    'DOZ':'dozen',
	'HL':'hectoliter',
	'SQUARE METER':'square meter',
	'SQM':'square meter',
	'SQ.MTR.':'square meter',
	'SQ. METRE':'square meter',
	'TONNE':'tonne',
	'T':'tonne',
	'KILOLITRE':'kiloliter',
	'KL': 'kilolitre',
	'SZT':'Polish sztych',
    'GALLON':'gallon',
    'GAL.':'gallon',
	'PAR':'pair',
	'M²':'square meter',
    'PCS':'pieces',
    'CM':'centimeters',
    'TON':'tonne',
    'ITEMS':'items',
    'UNIT':'unit',
    'M2':'square meter',
    'SM3':'standard cubic meter',
    'KGS':'kg',
    'PCE':'piece',
    'PIECE':'piece',
    'KILO':'kg',
    'KW':'kilowatt',
    'IMP.GAL': 'imperial gallon',
    'DAL':'dekaliter',
    'PRS':'pairs',
    'L':'liter',
    'LAA':'liters absolute alcohol'

}

operators = {
	'but not less than': '>=',
	'OR': 'OR',
	'+': 'AND',
    'AND':'AND',
	'PLUS':'AND',
	'MAX.':'max',
	'MIN.':'min',
    'MIN':'min',
	'MINIMUM':'min',
	'MAKSIMUM':"max",
	'QUOTA':'quota',
	'HIGHER':'>'
}


def make_corpus():
    """
    Creates dataset of all non-empty specific tariff lines
    """

    data_dir = "D:/Users/cmarciniak/Documents/macmap/data/unctad/specific"
    files = os.listdir(data_dir)
    df = pd.DataFrame()
    for f in files:
        try:
            file = os.path.join(data_dir,f)
            data = pd.read_csv(file,encoding='latin-1',dtype='object')
            subset = data[data.NonAdValorem!='   ']
            df = df.append(subset)
        except CParserError:
            print("Error ocurred in file: "+f)
    return df


def extract(dictionary,token):
    if dictionary[token]:
        return 1
    else:
        return -1


if __name__=="__main__":
    df = make_corpus()
    df.to_csv("specific_tariffs.csv")
