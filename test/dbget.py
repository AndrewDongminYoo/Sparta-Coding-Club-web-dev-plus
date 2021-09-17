from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from dbset import stocks
from pymongo import MongoClient
options = Options()
# options.headless = True
driver = Chrome(options=options)
driver.implicitly_wait(3)
# 파일을 만들어서 그대로 실행시킵니다!!
client = MongoClient("mongodb://localhost:27017/")
db = client.dbStock


def get_stock_info(code: str) -> list:
    url = f"https://finance.naver.com/item/main.nhn?code={code}"
    driver.get(url)
    price = driver.find_element_by_css_selector('#tab_con1 > div:nth-child(4) > table > tbody > tr:nth-child(2) > td > em:nth-child(1)').text
    si_total = driver.find_element_by_css_selector('#tab_con1 > div.first > table > tbody > tr.strong > td').text
    per = driver.find_element_by_css_selector('#_per').text
    db.stocks.update_one({"code": code}, {"$set": {"price": price, "capitalization": si_total, "PER": per}})
    return [price.strip(), si_total.strip(), per.strip()]


if __name__ == '__main__':
    for stock in stocks:
        get_stock_info(stock['code'])
    driver.quit()
