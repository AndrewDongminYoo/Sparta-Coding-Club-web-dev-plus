from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient('localhost', 27017)
# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
db = client.dbsparta_plus


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/matjip', methods=["GET"])
def get_matjip():
    # 맛집 목록을 반환하는 API
    matjip_list = list(db.restaurant.find({}, {'_id': False}))
    # matjip_list 라는 키 값에 맛집 목록을 담아 클라이언트에게 반환합니다.
    return jsonify({'result': 'success', 'matjip_list': matjip_list})


@app.route('/like_matjip', methods=["POST"])
def like_matjip():
    name_receive = request.form["name"]
    address_receive = request.form["address"]
    action_receive = request.form["action"]
    query1 = {"name": name_receive, "address": address_receive}
    if action_receive == "like":
        query2 = {"$set": {"liked": True}}
    else:
        query2 = {"$unset": {"liked": False}}
    db.restaurant.update_one(query1, query2)
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
