from selenium import webdriver
from bs4 import BeautifulSoup
import json
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests

client = MongoClient('localhost', 27017)
# client = MongoClient('내 AWS 아이피', 27017, username="아이디", password="비밀번호")
db = client.dbsparta_plus

limit = 741
programs = [
    "S01_V2000008533",
    "C01_B120144822",
    "C01_B120189770",
    "S01_V0000305532",
    "C01_B120145071",
    "C01_B120159120",
    "C01_B120177486",
    "S01_V2000010698"
]

categories = {
    "10": "베트남식",
    "11": "휴게소",
    "99": "기타",
    "02": "중식",
    "01": "한식",
    "04": "양식",
    "03": "일식",
    "05": "분식",
    "07": "카페",
    "08": "치킨",
    "09": "수산",
    "06": "베이커리"
}

programs = {"%M01_T40690": "생방송 오늘 저녁",
    "%S01_V2000008533": "백종원의 3대 천왕",
    "%S01_V0000338038": "생방송 투데이",
    "%C01_B120189770": "밥블레스유",
    "%MK1_PR752": "생생 정보마당",
    "%K02_T2014-0844": "2TV 생생정보",
    "%C01_B120144822": "수요미식회",
    "%MK1_PR769": "우리동네 맛집 탐방 미식클럽",
    "%K02_T2000-0037": "VJ특공대",
    "%J01_PR10010491": "밤도깨비",
    "%S11_22000012036": "외식하는 날 at Home",
    "%K01_T2000-0093": "6시 내고향",
    "%C01_B120145071": "2015 테이스티로드",
    "%S01_V0000305532": "생활의 달인",
    "%S01_V0000010090": "좋은아침",
    "%M01_T43347": "찾아라! 맛있는 TV",
    "%M01_T43003": "생방송 오늘 아침",
    "%J01_PR10010692": "TV정보쇼 오!아시스",
    "%M01_T80047": "#파워매거진",
    "%S06_V2000007049": "식객남녀 잘 먹었습니다",
    "%C01_B120159120": "2016 테이스티로드",
    "%C01_B120177486": "알쓸신잡  2",
    "%S11_22000011679": "외식하는 날 2",
    "%S01_V0000210215": "모닝와이드 3부",
    "%CA1_WPG2140064D": "먹거리X파일",
    "%S01_V2000010698": "백종원의 골목식당"}

def main():
    url = 'http://apis.sbs.co.kr/foodstar-api/1.1/search/list?location=11&offset=0&limit=' + str(limit)\
           + '&sort=view&latitude=0&longitude=0&programs='+','.join(programs)
    headers = {'ETag': 'W/"7fa7-rQ1yXuy135GclM1qqYUozJQkdio"'}

    req = requests.get(url, headers=headers)

    results = req.json()
    list_jip = []
    for result in results:
        restaurant = dict()
        if result.get('restaurantName'):
            restaurant['name'] = result.get('restaurantName')
            restaurant['category'] = categories.get(result.get('foodCategory_code'))
            if result.get('address'):
                restaurant['address'] = result.get('address')['roadAddress']
                restaurant['eng_address'] = result.get('address')['roadAddressEnglish']
                restaurant['lat'] = result.get('address')['latitude']
                restaurant['long'] = result.get('address')['longitude']
            restaurant['phone'] = result.get('phonenumber')
            restaurant['desc'] = result.get('description')
            if result.get('programs'):
                restaurant['program'] = result.get('programs')[0]['title']
                restaurant['pro_title'] = result.get('programs')[0]['subtitle']
            list_jip.append(restaurant)
            db.restaurant.insert_one(restaurant)
    print(len(list_jip))


if __name__ == "__main__":
    db.restaurant.delete_many({})
    main()
