# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class TaskOwnersTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_task_owners_test_case(self):
        driver = self.driver
        driver.get("http://192.168.3.120:8000/v7/")
        time.sleep(2)
        driver.find_element_by_link_text("Log in").click()
        time.sleep(2)
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("root")
        time.sleep(2)
        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("root12345")
        time.sleep(2)
        driver.find_element_by_id("submit-id-submit").click()
        time.sleep(2)
        driver.get("http://192.168.3.120:8000/v7/taskpackageowners/?regiontask_name=东南区域&taskpackage_name=task11")
        time.sleep(5)
        driver.find_element_by_link_text("2").click()
        time.sleep(3)
        driver.find_element_by_name("taskpackage_name").click()
        driver.find_element_by_name("taskpackage_name").clear()
        driver.find_element_by_name("taskpackage_name").send_keys("task12")
        time.sleep(2)
        driver.find_element_by_name("owner").click()
        driver.find_element_by_name("owner").clear()
        driver.find_element_by_name("owner").send_keys("worker7")
        time.sleep(2)
        driver.find_element_by_name("describe").click()
        driver.find_element_by_name("regiontask_name").click()
        driver.find_element_by_name("regiontask_name").clear()
        driver.find_element_by_name("regiontask_name").send_keys(u"东南区域")
        time.sleep(2)
        driver.find_element_by_id("content").click()
        time.sleep(5)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='任务区域'])[1]/following::button[1]").click()
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
