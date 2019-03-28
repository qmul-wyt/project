from flask import Flask, render_template, request, jsonify
import json
import requests_cache
import requests
from pprint import pprint

app = Flask(__name__)

url_template = 'https://api.exchangeratesapi.io/history?base=GBP&symbols=CAD,USD,CNY,EUR&start_at={start}&end_at={end}'

@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))

@app.route('/rates', methods=['GET'])
def rates():
    my_start = '2019-03-01'
    my_end = '2019-03-26'

    rates_url = url_template.format(start=my_start, end=my_end)

    resp = requests.get(rates_url)
    if resp.ok:
        rates = resp.json()
        pprint(rates)
    else:
        print(resp.reason)
    return jsonify(rates)

if __name__=="__main__":
    app.run(port=8080, debug=True)
