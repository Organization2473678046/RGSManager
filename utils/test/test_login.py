# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import constant


class Test_Login(unittest.TestCase):

    def setUp(self):
        # 初始化信息
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = constant.BASE_URL
        self.verificationErrors = []
        self.accept_next_alert = True
        self.username_admin = constant.USERNAME_ADMIN
        self.username_worker = constant.USERNAME_WORKER
        self.response_list_admin_message = ["200", self.username_admin, "true", "管理员"]
        self.response_list_worker_message = ["200", self.username_worker, "false", "作业员"]
        self.password = constant.PASSWORD
        self.error_username = "error"
        self.error_password = "error"
        self.response_permission = "身份认证信息未提供"

    def test_user(self):
        """测试各个接口权限,未登陆下无权限"""
        driver = self.driver
        driver.get(self.base_url)
        # 验证所有接口权限
        response_message_xpath = "/html/body/div/div[2]/div/div[2]/div[4]/pre/span[7]"
        for num in range(2, 10):
            url_xpath = "/html/body/div/div[2]/div/div[2]/div[4]/pre/a[{0}]/span".format(num)
            self.test_permission(url_xpath, response_message_xpath)

    def test_login_logout_admin(self):
        """测试登陆与登出,获取用户信息"""
        # 登录
        driver = self.driver
        driver.get(self.base_url)
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
        # 获取用户信息
        driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div[4]/pre/a[2]/span").click()
        text = driver.find_element_by_class_name("response-info").text
        # 接收response数据
        for response_text in self.response_list_admin_message:
            # 断言的状态码与用户信息
            self.assertIn(response_text, text, msg="返回用户信息{0}与预期不一致".format(text))
        driver.find_element_by_link_text(self.username_admin).click()
        driver.find_element_by_link_text("Log out").click()
        # 登出后判断是否残留权限
        text = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div[4]/pre/span[7]").text
        self.assertIn(self.response_permission, text, msg="返回的权限验证信息{0}与预期不一致".format(text))

    def test_login_logout_worker(self):
        """测试登陆与登出,获取用户信息"""
        # 登录
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Log in").click()
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.username_worker)
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.password)
        driver.find_element_by_id("id_password").send_keys(Keys.ENTER)
        # 通过获取登录后的用户名来断言是否登录成功
        text = driver.find_element_by_class_name("dropdown-toggle").text
        self.assertEqual(text, self.username_worker, msg=u"登录用户名错误或者没有捕捉到用户名")
        # 获取用户信息
        driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div[4]/pre/a[2]/span").click()
        text = driver.find_element_by_class_name("response-info").text
        # 接收response数据
        for response_text in self.response_list_worker_message:
            # 断言的状态码与用户信息
            self.assertIn(response_text, text, msg="返回用户信息{0}与预期不一致".format(text))
        driver.find_element_by_link_text(self.username_worker).click()
        driver.find_element_by_link_text("Log out").click()
        # 登出后判断是否残留权限
        text = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div[4]/pre/span[7]").text
        self.assertIn(self.response_permission, text, msg="返回的权限验证信息{0}与预期不一致".format(text))


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
        # 测试结束，恢复环境
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def test_permission(self, url_xpath, response_message_xpath):
        # 测试各接口权限
        driver = self.driver
        driver.find_element_by_xpath(url_xpath).click()
        text = driver.find_element_by_xpath(response_message_xpath).text
        self.assertIn(self.response_permission, text, msg="返回的权限验证信息{0}与预期不一致".format(text))
        driver.find_element_by_link_text("Api Root").click()




if __name__ == "__main__":
    unittest.main()
