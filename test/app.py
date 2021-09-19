from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.dbStock


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/base/codes', methods=['GET'])
def get_base_codes():
    codes = list(db.codes.find({}).distinct("group"))
    return jsonify(codes)


@app.route('/codes', methods=['GET'])
def get_codes():
    group = request.args.get('group')
    codes = list(db.codes.find({'group': group}, {'_id': False}))
    return jsonify(codes)


@app.route('/stocks', methods=['POST'])
def save_info():
    info = request.json
    stocks = list(db.stocks.find(info, {'_id': False}))
    db.searchs.insert_one(info)
    return jsonify(stocks)


@app.route('/stock/like', methods=['PUT'])
def set_like():
    info = request.json
    db.stocks.update_one({"code": info['code']}, {"$set": {"isLike": True}})
    return "success"


@app.route('/stock/unlike', methods=['PUT'])
def set_unlike():
    info = request.json
    db.stocks.update_one({"code": info['code']}, {"$set": {"isLike": False}})
    return "success"


@app.route('/stocks/like', methods=['GET'])
def get_stocks():
    stocks = list(db.stocks.find({"isLike": True}, {'_id': False}))
    return jsonify(stocks)


@app.route('/stock', methods=['GET'])
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
