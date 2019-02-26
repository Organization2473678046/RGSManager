# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
from random import randint


class Test_taskpackage(unittest.TestCase):


    def setUp(self):
        data_dict = {
            "name": "任务包{0}号".format(randint(99, 999999)),
            "owner": "worker",
            "mapnums": "1,2,3,4",
            "mapnumcounts": "4",
            "status": "1",
            "describe": "THIS IS DESCRIBE",
            "schedule": "一对多修改",
            "regiontask_name": "东南区域1800幅"
        }
        # 初始化信息
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = u"http://192.168.3.120:8000/v8/taskpackages/?regiontask_name=东南区域1800幅"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.username_admin = "root"
        self.username_worker = "worker"
        self.password = "root12345"
        self.error_username = "error"
        self.error_password = "error"
        self.response_permission = "身份认证信息未提供"
        self.response_worker = '"count":'
        self.data_dict = data_dict
        self.reponse_list = ["201", self.data_dict["name"], self.data_dict["regiontask_name"], self.data_dict["describe"]]
        self.order_data1_list = ["task{0}".format(num) for num in range(1, 11)]
        self.order_data2_list = ["task{0}".format(num) for num in range(11, 21)]

    def test_taskpackage_admin_create(self):
        """验证管理员创建记录并校验返回数据与输入数据一致性,测试任务包为task1,验证登出后权限"""
        # 验证管理员创建记录并校验
        # 验证登出后无权限访问数据
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
        driver.get(self.base_url)
        driver.find_element_by_name("name").click()
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys(self.data_dict.get("name"))
        driver.find_element_by_name("owner").click()
        driver.find_element_by_name("owner").clear()
        driver.find_element_by_name("owner").send_keys(self.data_dict.get("owner"))
        driver.find_element_by_name("mapnums").click()
        driver.find_element_by_name("mapnums").clear()
        driver.find_element_by_name("mapnums").send_keys(self.data_dict.get("mapnums"))
        driver.find_element_by_name("mapnumcounts").click()
        driver.find_element_by_name("mapnumcounts").clear()
        driver.find_element_by_name("mapnumcounts").send_keys(self.data_dict.get("mapnumcounts"))
        driver.find_element_by_name("status").click()
        driver.find_element_by_name("status").clear()
        driver.find_element_by_name("status").send_keys(self.data_dict.get("status"))
        driver.find_element_by_name("describe").click()
        driver.find_element_by_name("describe").clear()
        driver.find_element_by_name("describe").send_keys(self.data_dict.get("describe"))
        driver.find_element_by_name("schedule").click()
        driver.find_element_by_name("schedule").clear()
        driver.find_element_by_name("schedule").send_keys(self.data_dict.get("schedule"))
        driver.find_element_by_name("reallyname").click()
        driver.find_element_by_name("regiontask_name").click()
        driver.find_element_by_name("regiontask_name").clear()
        driver.find_element_by_name("regiontask_name").send_keys(self.data_dict.get("regiontask_name"))
        driver.find_element_by_xpath("//div[@id='post-object-form']/form/fieldset/div[11]/button").click()
        # 验证新记录是否正确
        text = driver.find_elements_by_class_name("prettyprint")[1].text
        for response_text in self.reponse_list:
            self.assertIn(response_text, text, msg="返回的权限验证信息{0}与预期不一致".format(text))
        # 登出后判断是否残留权限
        driver.find_element_by_link_text(self.username_admin).click()
        driver.find_element_by_link_text("Log out").click()
        text = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div[4]/pre/span[7]").text
        self.assertIn(self.response_permission, text, msg="返回的权限验证信息{0}与预期不一致".format(text))
        driver.find_element_by_link_text("Api Root").click()


    def test_taskpackage_list_admin(self):
        """验证按照id排序分页1，2页的数据一致性，登录权限为管理员，验证登出后权限"""
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

        # 验证按id排序后得到的数据是否为task1~task10
        driver.get(self.base_url + "&ordering=id")
        text = driver.find_elements_by_class_name("prettyprint")[1].text
        for order_data_text in self.order_data1_list:
            self.assertIn(order_data_text, text, msg="返回的排序数据{0}与预期不一致".format(text))

        # 验证按照id排序第二页数据
        driver.find_element_by_link_text("»").click()
        text = driver.find_elements_by_class_name("prettyprint")[1].text
        for order_data_text in self.order_data2_list:
            self.assertIn(order_data_text, text, msg="返回的排序数据{0}与预期不一致".format(text))

        # 登出后判断是否残留权限
        driver.find_element_by_link_text(self.username_admin).click()
        driver.find_element_by_link_text("Log out").click()
        text = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div[4]/pre/span[7]").text
        self.assertIn(self.response_permission, text, msg="返回的权限验证信息{0}与预期不一致".format(text))
        driver.find_element_by_link_text("Api Root").click()


    def test_taskpackage_list_worker(self):
        """验证作业员访问得到的数据，由于数据经常变动，此项数据暂不可使用"""
        driver = self.driver
        driver.get(self.base_url)
        # 作业员登录
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
        driver.get(self.base_url)
        # 验证返回数量应该为0
        text = driver.find_elements_by_class_name("prettyprint")[1].text
        self.assertIn(self.response_worker, text, msg="返回的权限验证信息{0}与预期不一致".format(text))

        # 登出后判断是否残留权限
        driver.find_element_by_link_text(self.username_worker).click()
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
        # 测试结束，清除环境
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)





if __name__ == "__main__":
    unittest.main()
