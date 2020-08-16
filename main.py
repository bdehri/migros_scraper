from bs4 import BeautifulSoup as bs
import requests

base_url="https://www.migros.com.tr"

category_suffix=["gazli-icecek-c-80"]


for category in category_suffix:
    i=1
    while True:
        endpoint=base_url+"/"+category+"?sayfa={}".format(i)
        r=requests.get(endpoint).text
        soup_output = bs(r,"html.parser")
        page_items_json=soup_output.findAll("script")[1]
        break