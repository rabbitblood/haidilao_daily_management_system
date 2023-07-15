"""
此文件为单独计算HDL工资使用
制作人：Hongming Wang
"""
import os
import time

import openpyxl
import selenium
import daily_work_automate
from selenium.webdriver.common.by import By

# accounts
ADP_ACC = "154772610"
ADP_PASS = "!!!Qz059522778157"


def get_all_time_and_pay():
    driver = daily_work_automate.init_web_driver()
    print("进入ADP网站")
    driver.get("https://workforcenow.adp.com")
    input("登入并点击回车键继续...")
    print("打开输出目标文件")
    target_xlsx_file_path = None
    for file in os.listdir("pay_data_file"):
        if "考勤" in file:
            target_xlsx_file_path = f"pay_data_file/{file}"
            break
    target_xlsx_wb = openpyxl.load_workbook(target_xlsx_file_path)
    target_xlsx_ws = target_xlsx_wb.active
    print("将ADP员工工时工资数据导入至目标文件")
    for row in range(2, target_xlsx_ws.max_row):
        if target_xlsx_ws[f"D{row}"].value is not None:
            print(target_xlsx_ws[f"D{row}"].value)
            try:
                get_rid_of_survey(driver)
                driver.find_element(By.XPATH, '//*[@id="employeeIdBarEmpListTooltipBtn"]').click()
                get_rid_of_survey(driver)
                time.sleep(5)
                get_rid_of_survey(driver)
                driver.find_element(By.XPATH, '//*[@id="idBarSscrollGrid_search"]').send_keys(target_xlsx_ws[f"D{row}"].value)
                get_rid_of_survey(driver)
                time.sleep(5)
                get_rid_of_survey(driver)
                driver.find_element(By.ID, "idBarSscrollGridIdCol_Id_1").click()
                get_rid_of_survey(driver)
                time.sleep(5)
                get_rid_of_survey(driver)
                try:
                    driver.find_element(By.XPATH, '//*[@id="aPay"]').click()
                    get_rid_of_survey(driver)
                    time.sleep(5)
                    get_rid_of_survey(driver)
                except:
                    pass
                get_rid_of_survey(driver)
                hours = driver.find_element(By.CLASS_NAME, "PayCodeFooter").find_element(By.CLASS_NAME, "NumericValuePayCode").text.split(":")
                pays = driver.find_element(By.CLASS_NAME, "PayCodeFooter").find_element(By.CLASS_NAME, "NumericValuePayCode.DollarsColumn").text
                target_xlsx_ws[f"E{row}"].value = float(f"{hours[0]}.{str(int(hours[1])/60).replace('0.', '')}")
                target_xlsx_ws[f"L{row}"].value = float(pays.replace(",", ""))
                print(target_xlsx_ws[f"E{row}"].value)
                print(target_xlsx_ws[f"L{row}"].value)
            except Exception as e:
                get_rid_of_survey(driver)
                driver.get("https://workforcenow.adp.com/theme/admin.html#/People_ttd_PeopleTabTimeAndAttendanceCategoryTLMWebIndividualTimeCard/PeopleTabTimeAndAttendanceCategoryTLMWebIndividualTimeCard")
                time.sleep(5)
                get_rid_of_survey(driver)
    target_xlsx_wb.save(target_xlsx_file_path)
    target_xlsx_wb.close()
    print("完成")


def get_rid_of_survey(driver):
    if check_element_exist(driver, '//*[@aria-label="Close"]'):
        print("killed a survey")
        driver.find_element(By.XPATH, '//*[@aria-label="Close"]').click()
        time.sleep(1)
        if check_element_exist(driver, '//*[@aria-label="Close"]'):
            driver.find_element(By.XPATH, '//*[@aria-label="Close"]').click()
            time.sleep(1)


def check_element_exist(driver, XPATH):
    try:
        if driver.find_element(By.XPATH, XPATH):
            return True
        else:
            return False
    except:
        return False


if __name__ == '__main__':
    get_all_time_and_pay()
