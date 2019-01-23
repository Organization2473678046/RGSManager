# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_user_test_case(self):
        driver = self.driver
        driver.get("http://192.168.3.120:8000/v7/")
        time.sleep(2)
        driver.find_element_by_link_text("Log in").click()
        time.sleep(3)
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("root")
        time.sleep(1)
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("root12345")
        time.sleep(1)
        driver.find_element_by_id("submit-id-submit").click()
        time.sleep(3)

        # 测试users接口
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)=concat('', '\"', '')])[1]/following::span[1]").click()
        time.sleep(5)
        driver.find_element_by_name("username").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("worker26")
        time.sleep(2)
        driver.find_element_by_name("password").click()
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("root12345")
        time.sleep(2)
        driver.find_element_by_name("reallyname").click()
        driver.find_element_by_name("reallyname").click()
        driver.find_element_by_name("reallyname").clear()
        driver.find_element_by_name("reallyname").send_keys(u"作业员26")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Raw data'])[1]/following::div[1]").click()
        time.sleep(5)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='真实姓名'])[1]/following::button[1]").click()
        time.sleep(5)
        # driver.find_element_by_link_text("root").click()
        # driver.find_element_by_link_text("Log out").click()
        time.sleep(2)

        # 测试user接口
        driver.get("http://192.168.3.120:8000/v7/")
        time.sleep(3)
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)=concat('', '\"', '')])[3]/following::span[1]").click()
        time.sleep(5)

        # 测试taskpackages接口
        driver.get("http://192.168.3.120:8000/v7/")
        time.sleep(2)
        driver.get("http://192.168.3.120:8000/v7/taskpackages/?regiontask_name=东南区域")
        time.sleep(3)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='}'])[2]/following::ul[1]").click()
        time.sleep(2)
        driver.find_element_by_link_text("2").click()
        time.sleep(2)
        driver.find_element_by_link_text("3").click()
        time.sleep(2)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='OPTIONS'])[1]/following::button[1]").click()
        time.sleep(1)
        driver.find_element_by_link_text(u"id - 正排序").click()
        time.sleep(3)
        driver.find_element_by_name("name").click()
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("tasktest1")
        time.sleep(1)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='主版本作业员'])[1]/following::span[1]").click()
        driver.find_element_by_name("owner").click()
        driver.find_element_by_name("owner").clear()
        driver.find_element_by_name("owner").send_keys("worker5")
        time.sleep(1)
        driver.find_element_by_name("mapnums").click()
        driver.find_element_by_name("mapnums").clear()
        driver.find_element_by_name("mapnums").send_keys("1,2,3,4,")
        time.sleep(2)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='图号集'])[1]/following::span[1]").click()
        driver.find_element_by_name("mapnumcounts").click()
        driver.find_element_by_name("mapnumcounts").clear()
        driver.find_element_by_name("mapnumcounts").send_keys("1")
        time.sleep(1)
        driver.find_element_by_name("file").clear()
        time.sleep(2)
        driver.find_element_by_name("file").send_keys("D:\\mmanageV7.0.tar")
        time.sleep(1)
        driver.find_element_by_name("status").click()
        time.sleep(1)
        driver.find_element_by_name("describe").clear()
        driver.find_element_by_name("describe").send_keys("22222")
        time.sleep(1)
        driver.find_element_by_name("regiontask_name").click()
        driver.find_element_by_name("regiontask_name").clear()
        driver.find_element_by_name("regiontask_name").send_keys(u"东南区域")
        time.sleep(3)
        driver.find_element_by_id("content").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='任务区域'])[1]/following::button[1]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='OPTIONS'])[1]/following::h1[1]").click()

        time.sleep(5)
        driver.get("http://192.168.3.120:8000/v7/taskpackages/?regiontask_name=东南区域")
        time.sleep(10)


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
