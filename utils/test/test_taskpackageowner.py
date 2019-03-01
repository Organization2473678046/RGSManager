# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import constant


class Test_taskpackageOwner(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = constant.BASE_URL + "taskpackageowners/?regiontask_name=东南区域1800幅&taskpackage_name=task11"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.username_admin = constant.USERNAME_ADMIN
        self.username_worker = constant.USERNAME_WORKER
        self.password = constant.PASSWORD
        self.response_permission = "身份认证信息未提供"
        self.data_dict = constant.TEST_DATA_1
        self.response_data = ['201', self.data_dict.get("taskpackage_name"),
                              '"owner": "{0}"'.format(self.data_dict.get("owner")),
                              self.data_dict.get("describe"),
                              self.data_dict.get("regiontask_name")]
        self.response_data2 = ['201', self.data_dict.get("taskpackage_name"),
                               '"owner": "{0}"'.format(self.data_dict.get("owner2")),
                               self.data_dict.get("describe"),
                               self.data_dict.get("regiontask_name")]

    def test_taskpackageowner(self):
        """验证@功能，管理员将task11任务包@给root，再@回worker"""
        driver = self.driver
        driver.get(self.base_url)
        # 管理员登录
        driver.find_element_by_link_text("Log in").click()
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.username_admin)
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.password)
        driver.find_element_by_id("id_password").send_keys(Keys.ENTER)
        # 通过获取登录后的用户名来断言是否登录成功
        text = driver.find_element_by_class_name("dropdown-toggle").text
        self.assertEqual(text, self.username_admin, msg=u"登录用户名错误或者没有捕捉到用户名")

        # 将worker名下的task11包@给root
        driver.get(self.base_url)
        driver.find_element_by_xpath("//div[@id='content']/div[2]/div[3]/pre").click()
        driver.find_element_by_name("taskpackage_name").click()
        driver.find_element_by_name("taskpackage_name").clear()
        driver.find_element_by_name("taskpackage_name").send_keys(self.data_dict.get("taskpackage_name"))
        driver.find_element_by_name("owner").click()
        driver.find_element_by_name("owner").clear()
        driver.find_element_by_name("owner").send_keys(self.data_dict.get("owner"))
        driver.find_element_by_name("describe").click()
        driver.find_element_by_name("describe").clear()
        driver.find_element_by_name("describe").send_keys(self.data_dict.get("describe"))
        driver.find_element_by_name("regiontask_name").click()
        driver.find_element_by_name("regiontask_name").clear()
        driver.find_element_by_name("regiontask_name").send_keys(self.data_dict.get("regiontask_name"))
        driver.find_element_by_xpath("//div[@id='post-object-form']/form/fieldset/div[5]/button").click()

        # 验证@返回数据
        text = driver.find_elements_by_class_name("prettyprint")[1].text
        for response_text in self.response_data:
            self.assertIn(response_text, text, msg="返回的验证信息{0}与预期不一致".format(text))

        # 将数据还原
        driver.find_element_by_name("owner").click()
        driver.find_element_by_name("owner").clear()
        driver.find_element_by_name("owner").send_keys(self.data_dict.get("owner2"))
        driver.find_element_by_xpath("//div[@id='post-object-form']/form/fieldset/div[5]/button").click()

        # 验证还原后数据
        text = driver.find_elements_by_class_name("prettyprint")[1].text
        for response_text in self.response_data2:
            self.assertIn(response_text, text, msg="返回的验证信息{0}与预期不一致".format(text))

        # 删除创建的@表记录
        SQL = "DELETE FROM taskpackages_taskpackageowner WHERE createtime>='2019-02-28 00:00:00'"
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
