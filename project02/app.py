from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests
app = Flask(__name__)

client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
db = client.dbsparta_plus_week2


@app.route('/')
def main():
    # DB 에서 저장된 단어 찾아서 HTML 에 나타내기
    return render_template("index.html")


@app.route('/detail/<keyword>')
def detail(keyword):
    url = f'https://owlbot.info/api/v4/dictionary/{keyword}'
    headers = {'Authorization': 'Token 76603619f99d7907e032157bede528157a590d1e'}
    req = requests.get(url, headers=headers)
    result = req.json()
    return render_template("detail.html", word=keyword, result=result)


@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기
    return jsonify({'result': 'success', 'msg': '단어 저장'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    return jsonify({'result': 'success', 'msg': '단어 삭제'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)