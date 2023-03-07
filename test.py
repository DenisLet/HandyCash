from scan import current_moment,get_link,handling
from parsing import check_link
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from send import errormsg,made_mistake
from send import bet_siska

options = webdriver.ChromeOptions()
options.add_argument('--mute-audio')
browser = webdriver.Chrome(options=options)
browser.get("https://www.handball24.com/")
switch_to_live = browser.find_element(By.CSS_SELECTOR, "div.filters__tab:nth-child(2) > div:nth-child(2)")
switch_to_live.click()
sleep(1)

scanset = set()


while True:
    try:
        matches = browser.find_elements(By.CSS_SELECTOR,"[id^='g_7']")

        for i in matches:
            try:

                time,score_one,score_two,score_line = handling(i)
                moment = current_moment(time)

                if moment:
                    link = get_link(i)
                    checker = 1
                    if link in scanset:
                        continue
                    scanset.add(link)
                    check_link(link, moment, score_one, score_two, checker, score_line)


            except Exception as fail:
                print('Mistake level 1')
                print(fail)
                sleep(2)
                continue

    except Exception as fail:
        print('Mistake level 2')
        print(fail)
        sleep(2)
        continue
    sleep(15)