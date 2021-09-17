import json

from dbget import get_stock_info
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
# from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.dbStock


@app.route('/')
def home():
    return render_template('stock.html')


# 백엔드
# 생략은 코드가 생략되었다는...
@app.route('/stock', methods=['POST'])
def save_info():
    print(request.form)
    market = request.form.get('market')
    sector = request.form.get('sector')
    tag = request.form.get('tag')
    query = {"sector": "sector-"+sector, "market": "market-"+market, "tag": "tag-"+tag}
    result = list(db.stocks.find(query, {'_id': False}))
    return jsonify({'message': '결과가 나왔습니다!', 'result': result})


@app.route('/company', methods=["GET"])
def search():
    code = request.form.get('code')
    [m, n, o] = get_stock_info(code)
    return jsonify({"message": "회사 정보", "result": {"m": m, "n": n, "o": o}})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
