from flask import Flask, render_template, request, jsonify
import json
import requests_cache
import requests
from pprint import pprint    

app = Flask(__name__)

url_template = 'https://api.exchangeratesapi.io/history?base=GBP&symbols=CAD,USD,CNY,EUR&start_at={start}&end_at={end}'
#use the exchage rate API but not completed

@app.route('/rates', methods=['GET'])
def rates():
    my_start = '2019-03-01'
    my_end = '2019-03-26'                #choose the the start and end time  

    rates_url = url_template.format(start=my_start, end=my_end)             #the completed url we use

    resp = requests.get(rates_url)   #use get method to download data
    if resp.ok:
        rates = resp.json()
        pprint(rates)
    else:
        print(resp.reason)
    return jsonify(rates)     # return json file 

if __name__=="__main__":
    app.run(port=8080, debug=True)
