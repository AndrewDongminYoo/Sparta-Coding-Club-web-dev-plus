from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time

driver = Chrome()
driver.implicitly_wait(5)
f = open("./hyun_soo/images.txt", mode="w", encoding="utf8", newline="")
target_list = []


def scroll_infinite():
    scroll_to_bottom = "window.scrollTo(0, document.body.scrollHeight);"
    get_window_height = "return document.body.scrollHeight"
    last_height = driver.execute_script(get_window_height)
    while True:
        driver.execute_script(scroll_to_bottom)
        time.sleep(2)
        new_height = driver.execute_script(get_window_height)
        target = driver.find_elements(
            By.XPATH, '//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div/div/a/div[1]/div[1]/img')
        for t in target:
            if t.get_attribute('src') not in target_list:
                target_list.append(t.get_attribute('src'))
                f.write(t.get_attribute('src'))
        if new_height == last_height:
            break
        last_height = new_height


def instagram_crawl(user_name):
    driver.get(f"https://www.instagram.com/{user_name}/")
    time.sleep(20)
    scroll_infinite()
    driver.quit()
    print(target_list)


if __name__ == '__main__':
    instagram_crawl("hyun_su_0105")

