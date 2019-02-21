# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.db.models import QuerySet
from django.test import TestCase
#
# # Create your tests here.
# if not os.environ.get("DJANGO_SETTINGS_MODULE"):
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RGSManager.settings")
# import django
# django.setup()
#
#
# if __name__ == '__main__':
#     from taskpackages.models import TaskPackage
#     from taskpackages.models import RegionTask
#     # obj1 = TaskPackage.objects.values("owner")
#     # print obj1
#     # obj = TaskPackage.objects.values("owner").distinct()
#     # print len(obj)
#     # print obj.count()
#     #
#     # print obj
#
#     taskpackage = TaskPackage.objects.get(name="task1",regiontask_name="东南区域")
#     print taskpackage
#     print taskpackage.regiontask_name
#
#     pass
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class TestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_case(self):
        driver = self.driver
        driver.get("http://192.168.3.120:8888/#/login?redirect=%2Fhome")
        driver.find_element_by_name("username").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("root")
        driver.find_element_by_name("password").click()
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("root12345")
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='全生命周期生产管理系统'])[2]/following::button[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='主页'])[1]/following::span[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='后台管理'])[1]/following::span[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::button[1]").click()
        driver.find_element_by_xpath(
            u"//*[@id='app']/div/div[1]/div[1]/div/ul/div[2]/li/ul/a/li/span/text()").click()
        driver.find_element_by_xpath(
             u"//*[@id='app']/div/div[1]/div[1]/div/ul/div[2]/li/ul/a/li/span/text()").clear()



        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='项目名称'])[2]/following::input[1]").send_keys(u"华北区域")
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='取消'])[1]/following::button[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='项目管理'])[1]/following::div[2]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='东南区域'])[1]/following::li[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='共 39 条'])[1]/following::li[5]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='共 39 条'])[1]/following::li[6]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='共 39 条'])[1]/following::li[7]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='共 39 条'])[1]/following::li[4]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='@'])[2]/following::button[2]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='task16'])[2]/following::button[1]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='@'])[1]/following::button[2]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='task2'])[2]/following::button[1]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='@'])[10]/following::button[2]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='task3'])[2]/following::button[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='任务包列表'])[1]/following::span[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='**按住Ctrl进行框选**'])[1]/following::canvas[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::input[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::input[1]").clear()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::input[1]").send_keys("task")
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::input[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::input[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::input[1]").clear()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::input[1]").send_keys("task37")
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::input[2]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::input[2]").clear()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::input[2]").send_keys(u"作业包37")
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::input[4]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='作业员5'])[1]/following::span[1]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='退出'])[1]/following::button[1]").click()

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
