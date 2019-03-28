from flask import Flask, request
from cassandra.cluster import Cluster

cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))

@app.route('/rates/<date>')
def profile(date):
    rows = session.execute( """Select * From rates.stats where date = '{}'""".format(date))

    for rates in rows:
        return('<h1>The rates in {} is {}!</h1>'.format(date,rates.eur))

    return('<h1>That date does not exist!</h1>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)