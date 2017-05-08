
import requests

h3_url = "https://comtrade.un.org/data/cache/classificationH3.json"
h4_url = "https://comtrade.un.org/data/cache/classificationH4.json"


h3 = requests.get(h3_url)
h4 = requests.get(h4_url)