from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = True
driver = Chrome(options=options)
driver.implicitly_wait(3)


def get_stock_info(code: str) -> tuple:
    url = f"https://finance.naver.com/item/main.nhn?code={code}"
    driver.get(url)
    price = driver.find_element_by_css_selector('#chart_area > div.rate_info > div > p.no_today').text.join('')
    si_total = driver.find_element_by_css_selector('#tab_con1 > div.first > table > tbody > tr.strong > td').text
    per = driver.find_element_by_css_selector('#_per').text
    return price.strip(), si_total.strip(), per.strip()


if __name__ == '__main__':
    get_stock_info("005930")
    driver.quit()
