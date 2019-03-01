# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import constant


class Test_taskpackageSchedule(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = constant.BASE_URL + "schedule/?regiontask_name=东南区域1800幅"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.username_admin = constant.USERNAME_ADMIN
        self.username_worker = constant.USERNAME_WORKER
        self.password = constant.PASSWORD
        self.data_dict = constant.TEST_DATA_SCHEDULE
        self.data_list1 = constant.TEST_LIST1_SCHEDULE
        self.data_list2 = constant.TEST_LIST2_SCHEDULE
        self.response_data = ["201", self.data_dict.get("schedule"), self.data_dict.get("regiontask_name")]
        self.response_permission = "身份认证信息未提供"


    def test_get_schedule(self):
        """获取进度，验证进度以及分页是否正确"""
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Log in").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.username_admin)
        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.password)
        driver.find_element_by_id("id_password").send_keys(Keys.ENTER)
        # 通过获取登录后的用户名来断言是否登录成功
        text = driver.find_element_by_class_name("dropdown-toggle").text
        self.assertEqual(text, self.username_admin, msg=u"登录用户名错误或者没有捕捉到用户名")

        # 验证返回第一页数据
        driver = self.driver
        driver.get(self.base_url)
        text = driver.find_elements_by_class_name("prettyprint")[1].text
        for response_text in self.data_list1:
            self.assertIn(response_text, text, msg="返回的验证信息{0}与预期不一致".format(text))

        # 验证第二页数据
        driver.find_element_by_link_text(u"»").click()
        text = driver.find_elements_by_class_name("prettyprint")[1].text
        for response_text in self.data_list2:
            self.assertIn(response_text, text, msg="返回的验证信息{0}与预期不一致".format(text))

        # 登出后判断是否残留权限
        driver.find_element_by_link_text(self.username_admin).click()
        driver.find_element_by_link_text("Log out").click()
        text = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div[4]/pre/span[7]").text
        self.assertIn(self.response_permission, text, msg="返回的权限验证信息{0}与预期不一致".format(text))
        driver.find_element_by_link_text("Api Root").click()

    def test_create_schedile(self):
        """创建进度，验证创建后返回信息是否正确"""
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Log in").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.username_admin)
        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.password)
        driver.find_element_by_id("id_password").send_keys(Keys.ENTER)
        # 通过获取登录后的用户名来断言是否登录成功
        text = driver.find_element_by_class_name("dropdown-toggle").text
        self.assertEqual(text, self.username_admin, msg=u"登录用户名错误或者没有捕捉到用户名")

        driver.find_element_by_name("schedule").click()
        driver.find_element_by_name("schedule").clear()
        driver.find_element_by_name("schedule").send_keys(self.data_dict.get("schedule"))
        driver.find_element_by_name("regiontask_name").click()
        driver.find_element_by_name("regiontask_name").clear()
        driver.find_element_by_name("regiontask_name").send_keys(self.data_dict.get("regiontask_name"))
        driver.find_element_by_xpath("//div[@id='post-object-form']/form/fieldset/div[3]/button").click()
        # 验证@返回数据
        text = driver.find_elements_by_class_name("prettyprint")[1].text
        for response_text in self.response_data:
            self.assertIn(response_text, text, msg="返回的验证信息{0}与预期不一致".format(text))
        SQL = "DELETE FROM taskpackages_taskpackagescheduleset WHERE schedule='{0}'".format(self.data_dict.get("schedule"))
        constant.clear(SQL=SQL)

        # 登出后判断是否残留权限
        driver.find_element_by_link_text(self.username_admin).click()
        driver.find_element_by_link_text("Log out").click()
        text = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div[4]/pre/span[7]").text
        self.assertIn(self.response_permission, text, msg="返回的权限验证信息{0}与预期不一致".format(text))
        driver.find_element_by_link_text("Api Root").click()


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
