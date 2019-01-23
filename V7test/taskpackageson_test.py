# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class TasksonTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_taskson_test_case(self):
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

        driver.get("http://192.168.3.120:8000/v7/taskpackagesons/?taskpackage_name=task1&regiontask_name=东南区域")
        time.sleep(3)
        driver.find_element_by_link_text("2").click()
        time.sleep(3)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Raw data'])[1]/following::div[1]").click()
        driver.find_element_by_name("taskpackage_name").click()
        driver.find_element_by_name("taskpackage_name").clear()
        time.sleep(3)
        driver.find_element_by_name("taskpackage_name").send_keys("task1")
        time.sleep(3)
        driver.find_element_by_name("describe").click()
        driver.find_element_by_name("describe").clear()
        driver.find_element_by_name("describe").send_keys(u"任务包子版本")
        time.sleep(3)
        # driver.find_element_by_name("file").click()
        driver.find_element_by_name("file").clear()
        time.sleep(2)
        driver.find_element_by_name("file").send_keys(u"E:\\下载的任务包\\Desktop.zip")
        time.sleep(3)
        driver.find_element_by_name("schedule").click()
        driver.find_element_by_name("schedule").clear()
        driver.find_element_by_name("schedule").send_keys(u"河环网修改")
        time.sleep(3)
        driver.find_element_by_name("regiontask_name").click()
        driver.find_element_by_name("regiontask_name").clear()
        driver.find_element_by_name("regiontask_name").send_keys(u"东南区域")
        time.sleep(3)
        driver.find_element_by_id("content").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='任务区域'])[1]/following::button[1]").click()
        time.sleep(10)
        driver.get("http://192.168.3.120:8000/v7/taskpackagesons/?taskpackage_name=task1&regiontask_name=东南区域")
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
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
