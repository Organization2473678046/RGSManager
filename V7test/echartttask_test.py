# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class EchartaskTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_echartask_test_case(self):
        driver = self.driver
        driver.get("http://192.168.3.120:8000/v7/")
        time.sleep(2)
        driver.find_element_by_link_text("Log in").click()
        time.sleep(2)
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()
        time.sleep(2)
        driver.find_element_by_id("id_username").send_keys("root")
        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("root12345")
        driver.find_element_by_id("id_password").send_keys(Keys.ENTER)
        time.sleep(5)
        driver.get("http://192.168.3.120:8000/v7/echarttaskpackages/?regiontask_name=东南区域")
        time.sleep(10)

        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='%'])[11]/following::pre[1]").click()
        # driver.find_element_by_xpath(
        #     "(.//*[normalize-space(text()) and normalize-space(.)='%'])[11]/following::pre[1]").click()
        # driver.find_element_by_xpath(
        # "(.//*[normalize-space(text()) and normalize-space(.)='Django REST framework'])[1]/following::b[1]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='OPTIONS'])[1]/following::h1[1]").click()

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
