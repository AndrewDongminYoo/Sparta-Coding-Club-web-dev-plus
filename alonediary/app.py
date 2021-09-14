import datetime

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import os
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbsparta
col = db.diary


# HTML 을 주는 부분
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(col.find({}, {'_id': False}))
    return jsonify({"message": '완료되었습니다.', 'diaries': diaries})


# API 역할을 하는 부분
@app.route('/diary', methods=['POST'])
def save_diary():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    time = now.strftime("%Y.%m.%d.")
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    file_receive = request.files["file_give"]
    ext = file_receive.content_type.split('/')[1]
    save_to = f'static/images/{timestamp}.{ext}'
    file_receive.save(save_to)
    doc = {
        'file': save_to,
        'title': title_receive,
        'content': content_receive,
        'time': time
    }
    col.insert_one(doc)
    return jsonify({"message": '완료되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

