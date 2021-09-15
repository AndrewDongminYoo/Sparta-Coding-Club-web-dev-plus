from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests
app = Flask(__name__)
client = MongoClient('localhost', 27017)
# client = MongoClient('localhost', 27017, username="아이디", password="비밀번호")
db = client.dbsparta


@app.route('/')
def main():
    words = list(db.dictionary.find({}, {"_id": False}))
    return render_template("index.html", words=words)


@app.route('/detail/<keyword>')
def detail(keyword):
    status = request.args.get('status')
    url = f'https://owlbot.info/api/v4/dictionary/{keyword}'
    headers = {'Authorization': 'Token 76603619f99d7907e032157bede528157a590d1e'}
    req = requests.get(url, headers=headers)
    if req.status_code != 200:
        return redirect(url_for("main", msg="e"))
    result = req.json()
    return render_template("detail.html", word=keyword, result=result, status=status)


@app.route('/api/save_word', methods=['POST'])
def save_word():
    word = request.form.get("word")
    definition = request.form.get("definition")
    doc = {'word': word, 'definition': definition}
    db.dictionary.insert_one(doc)
    return jsonify({'result': 'success', 'msg': f'{word} 저장되었습니다.'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    word_receive = request.form['word_give']
    db.dictionary.delete_one({"word": word_receive})
    db.examples.delete_many({"word": word_receive})
    return jsonify({'result': 'success', 'msg': f'word "{word_receive}" deleted'})


@app.route('/api/get_examples', methods=['GET'])
def get_exs():
    word_receive = request.args.get("word")
    result = list(db.examples.find({"word": word_receive}, {'_id': 0}))
    print(word_receive, len(result))

    return jsonify({'result': 'success', 'examples': result})


@app.route('/api/save_ex', methods=['POST'])
def save_ex():
    word_receive = request.form['word']
    example_receive = request.form['example']
    doc = {"word": word_receive, "example": example_receive}
    db.examples.insert_one(doc)
    return jsonify({'result': 'success', 'msg': f'example "{example_receive}" saved'})


@app.route('/api/delete_ex', methods=['POST'])
def delete_ex():
    word_receive = request.form['word']
    number_receive = int(request.form["number"])
    example = list(db.examples.find({"word": word_receive}))[number_receive]["example"]
    print(word_receive, example)
    db.examples.delete_one({"word": word_receive, "example": example})
    return jsonify({'result': 'success', 'msg': f'example #{number_receive} of "{word_receive}" deleted'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
