# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import constant


class Test_taskpackageSon(unittest.TestCase):

    def setUp(self):

        # 初始化信息
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = constant.BASE_URL + u"taskpackagesons/?regiontask_name=东南区域1800幅&taskpackage_name=task16"
        self.base_url2 = constant.BASE_URL + u"taskpackagesons/?regiontask_name=东南区域1800幅&taskpackage_name=task1"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.username_admin = constant.USERNAME_ADMIN
        self.username_worker = constant.USERNAME_WORKER
        self.password = constant.PASSWORD
        self.data_dict_admin = constant.TEST_DATA_ADMIN
        self.data_dict_worker = constant.TEST_DATA_WORKER
        self.file_path = constant.FILE_PATH
        self.response_permission = "身份认证信息未提供"
        self.reponse_list_admin = ["201", self.data_dict_admin["taskpackage_name"],
                                   self.data_dict_admin["regiontask_name"],
                                   self.data_dict_admin["describe"], self.data_dict_admin["user_username"],
                                   self.data_dict_admin["reallyname"], self.data_dict_admin["schedule"]]
        self.reponse_list_worker = ["201", self.data_dict_worker["taskpackage_name"],
                                    self.data_dict_worker["regiontask_name"],
                                    self.data_dict_worker["describe"], self.data_dict_worker["user_username"],
                                    self.data_dict_worker["reallyname"], self.data_dict_worker["schedule"]]

    def test_taskpackageson_admin(self):
        """验证管理员创建上传记录，对比记录准确性,管理员root,任务包task16,验证登出后无权访问数据"""
        driver = self.driver
        driver.get(self.base_url)
        # 登录并通过获取登录后的用户名来断言是否登录成功
        driver.find_element_by_link_text("Log in").click()
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.username_admin)
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.password)
        driver.find_element_by_id("id_password").send_keys(Keys.ENTER)
        text = driver.find_element_by_class_name("dropdown-toggle").text
        self.assertEqual(text, self.username_admin, msg=u"登录用户名错误或者没有捕捉到用户名")

        # 创建task16任务包子记录
        driver.get(self.base_url)
        driver.find_element_by_name("taskpackage_name").click()
        driver.find_element_by_name("taskpackage_name").clear()
        driver.find_element_by_name("taskpackage_name").send_keys(self.data_dict_admin.get("taskpackage_name"))
        driver.find_element_by_name("describe").clear()
        driver.find_element_by_name("describe").send_keys(self.data_dict_admin.get("describe"))
        driver.find_element_by_name("schedule").click()
        driver.find_element_by_name("schedule").clear()
        driver.find_element_by_name("schedule").send_keys(self.data_dict_admin.get("schedule"))
        driver.find_element_by_name("regiontask_name").click()
        driver.find_element_by_name("regiontask_name").clear()
        driver.find_element_by_name("regiontask_name").send_keys(self.data_dict_admin.get("regiontask_name"))
        driver.find_element_by_name("file").clear()
        driver.find_element_by_name("file").send_keys(self.file_path)
        driver.find_element_by_xpath("//div[@id='post-object-form']/form/fieldset/div[8]/button").click()

        # 验证上传成功后返回信息
        text = driver.find_elements_by_class_name("prettyprint")[1].text
        for response_text in self.reponse_list_admin:
            self.assertIn(response_text, text, msg="返回的验证信息{0}与预期不一致".format(text))

        # 清除测试记录
        SQL = "DELETE FROM taskpackages_taskpackageson WHERE taskpackage_name='{0}' AND version='{1}'".format(
            self.data_dict_admin.get("taskpackage_name"), 'v1.0')
        constant.clear(SQL=SQL)

        # 登出后判断是否残留权限
        driver.find_element_by_link_text(self.username_admin).click()
        driver.find_element_by_link_text("Log out").click()
        text = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div[4]/pre/span[7]").text
        self.assertIn(self.response_permission, text, msg="返回的权限验证信息{0}与预期不一致".format(text))
        driver.find_element_by_link_text("Api Root").click()

    def test_taskpackageson_worker_false(self):
        """验证作业员上传不属于自己的任务包,作业员worker,任务包task16，验证登出后权限"""
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
        self.assertEqual(text, self.username_worker)

        driver.get(self.base_url)
        driver.find_element_by_name("taskpackage_name").click()
        driver.find_element_by_name("taskpackage_name").clear()
        driver.find_element_by_name("taskpackage_name").send_keys(self.data_dict_admin.get("taskpackage_name"))
        driver.find_element_by_name("describe").clear()
        driver.find_element_by_name("describe").send_keys(self.data_dict_admin.get("describe"))
        driver.find_element_by_name("schedule").click()
        driver.find_element_by_name("schedule").clear()
        driver.find_element_by_name("schedule").send_keys(self.data_dict_admin.get("schedule"))
        driver.find_element_by_name("regiontask_name").click()
        driver.find_element_by_name("regiontask_name").clear()
        driver.find_element_by_name("regiontask_name").send_keys(self.data_dict_admin.get("regiontask_name"))
        driver.find_element_by_name("file").clear()
        driver.find_element_by_name("file").send_keys("C:\\Users\\Administrator\\Desktop\\chardet-master.zip")
        driver.find_element_by_xpath("//div[@id='post-object-form']/form/fieldset/div[8]/button").click()

        text = driver.find_elements_by_class_name("prettyprint")[1].text
        self.assertIn("用户 {0} 无权限".format(self.username_worker), text, msg="返回的验证信息{0}与预期不一致".format(text))
        driver.find_element_by_link_text(self.username_worker).click()
        driver.find_element_by_link_text("Log out").click()
        text = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div[4]/pre/span[7]").text
        self.assertIn(self.response_permission, text, msg="返回的权限验证信息{0}与预期不一致".format(text))
        driver.find_element_by_link_text("Api Root").click()

    def test_taskpackageson_worker_true(self):
        """验证作业员上传属于自己的作业包,作业员worker,任务包task1"""
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
        self.assertEqual(text, self.username_worker)

        # 作业员上传属于自己的作业包子版本
        driver.get(self.base_url2)
        driver.find_element_by_name("taskpackage_name").click()
        driver.find_element_by_name("taskpackage_name").clear()
        driver.find_element_by_name("taskpackage_name").send_keys(self.data_dict_worker.get("taskpackage_name"))
        driver.find_element_by_name("describe").clear()
        driver.find_element_by_name("describe").send_keys(self.data_dict_worker.get("describe"))
        driver.find_element_by_name("schedule").click()
        driver.find_element_by_name("schedule").clear()
        driver.find_element_by_name("schedule").send_keys(self.data_dict_worker.get("schedule"))
        driver.find_element_by_name("regiontask_name").click()
        driver.find_element_by_name("regiontask_name").clear()
        driver.find_element_by_name("regiontask_name").send_keys(self.data_dict_worker.get("regiontask_name"))
        driver.find_element_by_name("file").clear()
        driver.find_element_by_name("file").send_keys(self.file_path)
        driver.find_element_by_xpath("//div[@id='post-object-form']/form/fieldset/div[8]/button").click()

        # 验证返回数据是否正确
        text = driver.find_elements_by_class_name("prettyprint")[1].text
        for response_text in self.reponse_list_worker:
            self.assertIn(response_text, text, msg="返回的验证信息{0}与预期不一致".format(text))

        # 清除测试记录
        SQL = "DELETE FROM taskpackages_taskpackageson WHERE taskpackage_name='{0}' AND version='{1}'".format(
            self.data_dict_worker.get("taskpackage_name"), 'v4.0')
        constant.clear(SQL=SQL)

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
    pass
