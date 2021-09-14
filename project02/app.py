from flask import Flask, render_template
import requests
app = Flask(__name__)


@app.route('/')
def main():
    myname = "동민"
    return render_template("index.html", name=myname)


@app.route('/detail')
def detail():
    response = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99').json()
    rows = response['RealtimeCityAir']['row']
    return render_template("detail.html", rows=rows)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)