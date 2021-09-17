from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.dbStock


@app.route('/')
def home():
    return render_template('stock.html')


@app.route('/stock', methods=['POST'])
def save_info():
    print(request.form)
    market = request.form.get('market')
    sector = request.form.get('sector')
    tag = request.form.get('tag')
    query = {"sector": "sector-"+sector, "market": "market-"+market, "tag": "tag-"+tag}
    print(query)
    result = list(db.stocks.find(query, {'_id': False}))
    print(result)
    return jsonify({'message': '결과가 나왔습니다!', 'result': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
