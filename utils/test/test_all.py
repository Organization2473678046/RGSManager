# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import unittest
import HTMLTestRunner


from utils.test.test_login import Test_Login
from utils.test.test_taskpackage import Test_taskpackage
from utils.test.test_taskpackageregiontask import Test_taskpackageRegiontask
from utils.test.test_taskpackageson import Test_taskpackageSon
from utils.test.test_taskpackageowner import Test_taskpackageOwner
from utils.test.test_taskpackageschedule import Test_taskpackageSchedule





if __name__ == "__main__":
    # 测试套件
    testunit = unittest.TestSuite()
    # 添加测试用例到测试套件中
    # testunit.addTest(Test_Login("test_user"))
    # testunit.addTest(Test_Login("test_login_logout_admin"))
    # testunit.addTest(Test_Login("test_login_logout_worker"))
    # testunit.addTest(Test_taskpackage("test_taskpackage_create_admin"))
    # testunit.addTest(Test_taskpackage("test_taskpackage_list_admin"))
    # testunit.addTest(Test_taskpackage("test_taskpackage_list_worker"))
    # testunit.addTest(Test_taskpackageSon("test_taskpackageson_admin"))
    # testunit.addTest(Test_taskpackageSon("test_taskpackageson_worker_false"))
    # testunit.addTest(Test_taskpackageSon("test_taskpackageson_worker_true"))
    # testunit.addTest(Test_taskpackageOwner("test_taskpackageowner"))
    # testunit.addTest(Test_taskpackageSchedule("test_get_schedule"))
    # testunit.addTest(Test_taskpackageSchedule("test_create_schedile"))
    testunit.addTest(Test_taskpackageRegiontask("test_regiontask_create"))

    # 测试报告
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    filename = 'D:\\code\\RGSManager\\test_html\\result_{0}.html'.format(now)
    fp = file(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'测试报告',
        description=u'测试用例包含用户接口,主任务包接口，子任务包接口')
    # 运行测试用例
    runner.run(testunit)
    fp.close()
