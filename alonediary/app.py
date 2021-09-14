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
    index = 0
    if 'title_give' in request.form.keys():
        title_receive = request.form['title_give']
    else:
        title_receive = ""
    content_receive = request.form['content_give']
    save_to = ""
    while title_receive and request.files:
        save_to = f'static/images/{title_receive}{str(index).zfill(4)}.png'
        if os.path.isfile(save_to):
            index += 1
            save_to = f'static/images/{title_receive}{str(index).zfill(4)}.png'
        else:
            break
    if request.files and save_to:
        file_receive = request.files["file_give"]
        file_receive.save(save_to)
    else:
        file_receive = ""
    doc = {
       'file': save_to,
       'title': title_receive,
       'content': content_receive
    }
    col.insert_one(doc)
    return jsonify({"message": '완료되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

