from dbget import get_stock_info
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
# from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
app = Flask(__name__)
client = MongoClient('localhost', 27017)
# client = MongoClient('내 AWS 아이피', 27017, username="아이디", password="비밀번호")
db = client.dbsparta_plus





# 백엔드
# 생략은 코드가 생략되었다는...
@app.route('/stock', methods = ['POST'])
def save_info():
    info = request.json
    ##생략
		return jsonify(stocks)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
