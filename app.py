from flask import Flask, request, jsonify
from cassandra.cluster import Cluster

cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))

@app.route('/rates/<date>/<currency>')
def profile(date,currency):
    rows = session.execute( """Select * From rates.stats where date = '{}'""".format(date))
    if currency == 'cad':
        for rates in rows:
            #return('<h1>The exchange rates between GBP and CAD in {} is {}!</h1>'.format(date,rates.cad))
            return jsonify(rates)
    elif currency == 'usd':
        for rates in rows:
            return('<h1>The exchange rates between GBP and USD in {} is {}!</h1>'.format(date,rates.usd))
            return jsonify(rates)
    elif currency == 'cny':
        for rates in rows:
            return('<h1>The exchange rates between GBP and CNY in {} is {}!</h1>'.format(date,rates.cny))
            return jsonify(rates)
    elif currency == 'eur':
        for rates in rows:
            return('<h1>The exchange rates between GBP and EUR in {} is {}!</h1>'.format(date,rates.eur))
            return jsonify(rates)
    return('<h1>That date does not exist!</h1>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
