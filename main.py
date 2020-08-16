from flask import Flask
from flask import Response
from datetime import datetime
from bs4 import BeautifulSoup as bs
import requests
import json
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def parse():
    resp = Response(parse_migros())
    date = datetime.now().strftime("%d-%m-%Y")
    fileName = "migros-icecek_" + date + ".csv"
    resp.headers["content-disposition"] = "attachment; filename=" + fileName
    return resp


def parse_migros():
    print("parse_migros")

    base_url="https://www.migros.com.tr"

    category_suffix=["gazli-icecek-c-80","gazsiz-icecek-c-81","cay-c-475","kahve-c-476","su-c-84","maden-suyu-c-85"]

    csv_string = "İsim,Kategori,Fiyat,url,Marka\n"
    for category in category_suffix:
        i=1
        while True:
            endpoint=base_url+"/"+category+"?sayfa={}".format(i)
            print(endpoint)
            r=requests.get(endpoint).text
            soup_output = bs(r,"html.parser")
            page_items_string_raw=soup_output.findAll("script")[1].string
            page_items_json_raw=json.loads(page_items_string_raw)
            items_json_array=page_items_json_raw["mainEntity"]["offers"]["itemOffered"]
            
            if len(items_json_array)==0:
                break

            for item in items_json_array:
                csv_string += get_csv_string(item)

            i+=1

    return csv_string

def get_csv_string(item):
    return "\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"\n".format(item["name"], item["category"], item["offers"]["price"], item["url"], item["brand"]["name"])
