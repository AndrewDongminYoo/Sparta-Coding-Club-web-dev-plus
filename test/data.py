from selenium.webdriver import Chrome
from pymongo import MongoClient
import requests

# driver = Chrome()
# driver.implicitly_wait(3)
# 파일을 만들어서 그대로 실행시킵니다!!
client = MongoClient("mongodb://localhost:27017/")
db = client.dbStock

db.codes.delete_many({})
codes = [
    {"group": "market", "code": "market-1", "name": "코스피"},
    {"group": "market", "code": "market-2", "name": "코스닥"},
    {"group": "sector", "code": "sector-1", "name": "반도체와반도체장비"},
    {"group": "sector", "code": "sector-2", "name": "양방향미디어와서비스"},
    {"group": "sector", "code": "sector-3", "name": "자동차"},
    {"group": "tag", "code": "tag-1", "name": "메모리"},
    {"group": "tag", "code": "tag-2", "name": "플랫폼"},
    {"group": "tag", "code": "tag-3", "name": "자동차부품"},
    {"group": "tag", "code": "tag-4", "name": "전기차"},
]
db.codes.insert_many(codes)

db.stocks.delete_many({})
stocks = [
    {"name": "하나머티리얼즈", "code": "166090", "sector": "sector-1", "market": "market-2", "tag": "tag-1"},
    {"name": "에코플라스틱", "code": "038110", "sector": "sector-3", "market": "market-2", "tag": "tag-3"},
    {"name": "디아이씨", "code": "092200", "sector": "sector-3", "market": "market-1", "tag": "tag-3"},
    {"name": "뉴파워플라즈마", "code": "144960", "sector": "sector-1", "market": "market-1", "tag": "tag-1"},
    {"name": "기아차", "code": "000270", "sector": "sector-3", "market": "market-1", "tag": "tag-3"},
    {"name": "퓨쳐스트림네트웍스", "code": "214270", "sector": "sector-2", "market": "market-2", "tag": "tag-2"},
    {"name": "삼성전자", "code": "005930", "sector": "sector-1", "market": "market-1", "tag": "tag-1"},
    {"name": "SK 하이닉스", "code": "000660", "sector": "sector-1", "market": "market-1", "tag": "tag-1"},
    {"name": "리노공업", "code": "058470", "sector": "sector-1", "market": "market-2", "tag": "tag-1"},
    {"name": "DB 하이텍", "code": "000990", "sector": "sector-1", "market": "market-1", "tag": "tag-1"},
    {"name": "솔브레인", "code": "357780", "sector": "sector-1", "market": "market-2", "tag": "tag-1"},
    {"name": "카카오", "code": "035720", "sector": "sector-2", "market": "market-1", "tag": "tag-2"},
    {"name": "네이버", "code": "035420", "sector": "sector-2", "market": "market-1", "tag": "tag-2"},
    {"name": "아프리카 TV", "code": "067160", "sector": "sector-2", "market": "market-2", "tag": "tag-3"},
    {"name": "키다리스튜디오", "code": "020120", "sector": "sector-2", "market": "market-1", "tag": "tag-2"},
    {"name": "현대차", "code": "005380", "sector": "sector-3", "market": "market-1", "tag": "tag-4"},
]
db.stocks.insert_many(stocks)


def get_stock_info_api(code: str) -> list:
    url = f'https://m.stock.naver.com/api/stock/{code}/integration'
    headers = {'accept': 'application/json', 'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'origin': 'https://m.stock.naver.com',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

    req = requests.get(url, headers=headers)
    data = req.json()['totalInfos']
    highPrice = data[2]["value"]
    accumulatedTradingVolume = data[4]["value"]
    marketValue = data[6]["value"]
    PER = data[10]["value"]
    set_query = {
        "price": highPrice,
        "accumulatedTradingVolume": accumulatedTradingVolume,
        "capitalization": marketValue,
        "PER": PER
    }
    db.stocks.update_one({"code": code}, {"$set": set_query})
    return list(db.stocks.find({"code": code}, {"_id": False}))


if __name__ == '__main__':
    for stock in stocks:
        get_stock_info_api(stock['code'])
