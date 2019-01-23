# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class TaskTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_task_test_case(self):
        driver = self.driver
        driver.get("http://192.168.3.120:8000/v7/taskpackages/?regiontask_name=%E4%B8%9C%E5%8D%97%E5%8C%BA%E5%9F%9F")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='}'])[2]/following::ul[1]").click()
        driver.find_element_by_link_text("2").click()
        driver.find_element_by_link_text("3").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='OPTIONS'])[1]/following::button[1]").click()
        driver.find_element_by_link_text(u"id - 正排序").click()
        driver.find_element_by_name("name").click()
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("tasktest")
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='主版本作业员'])[1]/following::span[1]").click()
        driver.find_element_by_name("owner").click()
        driver.find_element_by_name("owner").clear()
        driver.find_element_by_name("owner").send_keys("worker5")
        driver.find_element_by_name("mapnums").click()
        driver.find_element_by_name("mapnums").clear()
        driver.find_element_by_name("mapnums").send_keys("1,2,3,4")
        driver.find_element_by_name("mapnumcounts").click()
        driver.find_element_by_name("mapnums").click()
        driver.find_element_by_name("mapnums").clear()
        driver.find_element_by_name("mapnums").send_keys("1,2,3,4,")
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='图号集'])[1]/following::span[1]").click()
        driver.find_element_by_name("mapnumcounts").click()
        driver.find_element_by_name("mapnumcounts").clear()
        driver.find_element_by_name("mapnumcounts").send_keys("-1")
        driver.find_element_by_name("mapnumcounts").click()
        driver.find_element_by_name("mapnumcounts").clear()
        driver.find_element_by_name("mapnumcounts").send_keys("1")
        driver.find_element_by_name("status").click()
        driver.find_element_by_name("file").clear()
        driver.find_element_by_name("file").send_keys("C:\\fakepath\\mmanageV5.0.tar")
        driver.find_element_by_name("status").click()
        driver.find_element_by_name("describe").clear()
        driver.find_element_by_name("describe").send_keys("22222")
        driver.find_element_by_name("regiontask_name").click()
        driver.find_element_by_name("regiontask_name").clear()
        driver.find_element_by_name("regiontask_name").send_keys(u"东南区域")
        driver.find_element_by_id("content").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='任务区域'])[1]/following::button[1]").click()
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
