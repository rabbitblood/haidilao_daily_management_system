# test
import os

import openpyxl
from selenium.webdriver.common.by import By
import daily_work_automate
import sms_handler
import time
import re

FANTUAN_USERNAME = daily_work_automate.FANTUAN_USERNAME
FANTUAN_PASSWORD = daily_work_automate.FANTUAN_PASSWORD

ft_amounts = 0
ft_fee = 0
driver = daily_work_automate.init_web_driver()
print("登入饭团账号")
driver.get('https://pos.fantuan.ca/')
driver.find_element(By.XPATH, '//*[@placeholder="用户名"]').send_keys(FANTUAN_USERNAME)
driver.find_element(By.XPATH, '//*[@placeholder="密码"]').send_keys(FANTUAN_PASSWORD)
driver.find_element(By.XPATH, '//*[@type="submit"]').click()
time.sleep(2)
try:
    driver.find_element(By.CLASS_NAME, 'send_smsCode_btn').click()
    time.sleep(30)
    driver.find_element(By.XPATH, '//*[@type="tel"]').send_keys(re.findall("\d{6}", sms_handler.get_most_recent_message())[0])
    driver.find_element(By.CLASS_NAME, 'verify_smsCode_btn').click()
    time.sleep(5)
except:
    pass
driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div/div[2]/div/div/div[2]').click()
time.sleep(3)
left_right_buttons = driver.find_elements(By.XPATH, '//*[@class="__1ZaR-"]')
left_right_buttons[1].click()
time.sleep(3)
orders = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/div/div/div[4]/div[1]/div/div[2]/div')
for item in orders:
    split_items = item.text.split()
    if len(split_items) > 1:
        if int(split_items[3].split(":")[0]) > 10:
            item.click()
            time.sleep(0.5)
            amounts = driver.find_elements(By.XPATH, '//*[@class="__33MCY __2QIVY"]')
            fantuan_transfer = amounts[2].text.split()[1].replace("$", "")
            fantuan_fee = amounts[1].text.split()[1].replace("-$", "")
            ft_amounts += float(fantuan_transfer)
            ft_fee += float(fantuan_fee)
left_right_buttons = driver.find_elements(By.XPATH, '//*[@class="__1ZaR-"]')
left_right_buttons[2].click()
time.sleep(3)
orders = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/div/div/div[4]/div[1]/div/div[2]/div')
for item in orders:
    split_items = item.text.split()
    print(split_items)
    if len(split_items) > 1:
        if int(split_items[3].split(":")[0]) < 10:
            item.click()
            time.sleep(0.5)
            amounts = driver.find_elements(By.XPATH, '//*[@class="__33MCY __2QIVY"]')
            fantuan_transfer = amounts[2].text.split()[1].replace("$", "")
            fantuan_fee = amounts[1].text.split()[1].replace("-$", "")
            print(fantuan_transfer)
            print(fantuan_fee)
            ft_amounts += float(fantuan_transfer)
            ft_fee += float(fantuan_fee)
print(ft_amounts)
print(ft_fee)


input("...")
