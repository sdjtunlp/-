from selenium import webdriver
import numpy as np
import random
import datetime
import time

today = str(datetime.date.today())
today = today.split("-")
weekday = datetime.date(int(today[0]), int(today[1]), int(today[2])).isoweekday()

drive_path = "E:\miniconda3\envs\gspy3.6\Scripts\chromedriver.exe"

username_xpath = "/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/form/div[1]/nz-input-group/input"
password_xpath = "/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/form/div[2]/nz-input-group/input"
login_path = "/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/form/div[6]/div/button"

Campus_xpath = '//*[@id="fieldXQ-0"]'
On_campus_xpath = '//*[@id="fieldSFLKXX-0"]'
nucleic_acid_xpath0 = '//*[@id="fieldDESFHS-0"]'  # 做了核酸
nucleic_acid_xpath1 = '//*[@id="fieldDESFHS-1"]'  # 没做核酸

morning_xpath = '//*[@id="V1_CTRL5"]'
afternoon_xpath = '//*[@id="V1_CTRL6"]'
evening_xpath = '//*[@id="V1_CTRL7"]'

fever_xpath = '//*[@id="fieldSFFR-1"]'
roommates_xpath = '//*[@id="fieldGTJZR-1"]'
submit_parent_path  = '//*[@id="form_command_bar"]/li[1]'

remark_parent_xpath = '/html/body/div[6]'


login_url = 'https://cas1.sdjtu.edu.cn/cas/login?service=https:%2F%2Ftaskcenter.sdjtu.edu.cn%2Finfoplus%2Flogin%3FretUrl%3Dhttps%253A%252F%252Ftaskcenter.sdjtu.edu.cn%252Finfoplus%252Fform%252FXSYRSJLBG%252Fstart'
username = ''
password = ''

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# driver = webdriver.Chrome(drive_path, options=options)

driver = webdriver.Chrome(drive_path)
# driver = webdriver.Edge("E:\miniconda3\envs\gspy3.6\Scripts\msedgedriver.exe")
driver.get(login_url)
time.sleep(3)

# 登录
driver.find_element_by_xpath(username_xpath).send_keys(username)
driver.find_element_by_xpath(password_xpath).send_keys(password)
driver.find_element_by_xpath(login_path).click()
time.sleep(3)

# 填写数据
driver.find_element_by_xpath(Campus_xpath).click()
driver.find_element_by_xpath(On_campus_xpath).click()

if weekday in [2, 5]:
    driver.find_element_by_xpath(nucleic_acid_xpath0).click()
else:
    driver.find_element_by_xpath(nucleic_acid_xpath1).click()

body_temperature_morning = np.linspace(36.1, 36.3, 3)
body_temperature_afternoon = np.linspace(36.4, 36.6, 3)
body_temperature_evening = np.linspace(36.3, 36.6, 3)

random.shuffle(body_temperature_morning)
random.shuffle(body_temperature_afternoon)
random.shuffle(body_temperature_evening)



# 体温填写
driver.find_element_by_xpath(morning_xpath).send_keys(str(body_temperature_morning[0]))
driver.find_element_by_xpath(afternoon_xpath).send_keys(str(body_temperature_afternoon[0]))
driver.find_element_by_xpath(evening_xpath).send_keys(str(body_temperature_evening[0]))

#本人是否发烧
driver.find_element_by_xpath(fever_xpath).click()
#舍友是否发烧
driver.find_element_by_xpath(roommates_xpath).click()

#获取提交xpath
t = driver.find_element_by_xpath(submit_parent_path)
page_source = t.parent.page_source
pos_submit_xpath = page_source.find('infoplus_action')
submit_xpath = '//*[@id' + page_source[pos_submit_xpath-2:pos_submit_xpath+23] + ']'
#//*[@id="infoplus_action_8896_1"]

#提交
driver.find_element_by_xpath(submit_xpath).click()
time.sleep(1)

#备注

pos_remark_xpath = page_source.find('dialog_container')
remark_xpath = '//*[@id' + page_source[pos_remark_xpath-2:pos_remark_xpath+24] + ']' + '/div[2]/button[1]'
#//*[@id="dialog_container_589914"]/div[2]/button[1]

driver.find_element_by_xpath(remark_xpath).click()

driver.close()
driver.quit()







