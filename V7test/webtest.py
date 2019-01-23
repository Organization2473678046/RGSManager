# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class QianduanTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_qianduan_test_case(self):
        driver = self.driver
        driver.get("http://192.168.3.120:8888/#/login?redirect=%2Fhome")
        driver.find_element_by_name("username").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("root")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("root12345")
        driver.find_element_by_name("password").send_keys(Keys.ENTER)
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='后台管理'])[1]/following::i[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='后台管理'])[1]/following::li[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='东南区域'])[1]/following::i[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='东南区域'])[1]/following::li[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='共 40 条'])[1]/following::li[5]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='共 40 条'])[1]/following::li[6]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='@'])[2]/following::button[2]").click()
        time.sleep(5)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='task33'])[2]/following::button[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='无'])[4]/following::button[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='为task5指定作业员'])[1]/following::button[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='@'])[4]/following::button[3]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='@记录'])[2]/following::button[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='@'])[8]/following::button[3]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='@记录'])[2]/following::button[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='搜索'])[1]/following::i[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='搜索'])[1]/following::i[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='共 40 条'])[1]/following::li[5]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='@'])[1]/following::button[3]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='@记录'])[2]/following::button[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='@'])[3]/following::button[2]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='task13'])[2]/following::button[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='任务包划分'])[1]/following::span[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::i[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='作业员任务包处理数量'])[1]/following::li[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='任务包统计'])[1]/following::div[2]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='管理'])[1]/following::li[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='东南区域'])[1]/following::span[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='主页'])[1]/following::div[2]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='后台管理'])[1]/following::li[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::button[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='项目名称'])[2]/following::input[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='项目名称'])[2]/following::input[1]").clear()
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='项目名称'])[2]/following::input[1]").send_keys(u"京津冀区域")
        time.sleep(3)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='取消'])[1]/following::button[1]").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        # self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
