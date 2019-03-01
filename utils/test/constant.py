# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from random import randint
import psycopg2


# 基础路由
BASE_URL = U"http://192.168.3.120:8081/v9/"

# 管理员用户名称
USERNAME_ADMIN = u"root"

# 作业员名称
USERNAME_WORKER = u"worker"

# 密码（通用）
PASSWORD = u"root12345"

# 测试文件路径
FILE_PATH = "C:\\Users\\Administrator\\Desktop\\Everything-v1.4.1.925.rar"

# 主任务包所需数据
TEST_DATA = {
    "name": "任务包{0}号".format(randint(99, 999999)),
    "owner": "worker",
    "mapnums": "1,2,3,4",
    "mapnumcounts": "4",
    "status": "1",
    "describe": "THIS IS DESCRIBE",
    "schedule": "等高线拼接",
    "regiontask_name": "东南区域1800幅"
}

# 子任务包所需要数据
TEST_DATA_ADMIN = {
    "taskpackage_name": "task16",
    "user_username": "root",
    "describe": "THIS IS DESCRIBE",
    "schedule": "一对多修改",
    "regiontask_name": "东南区域1800幅",
    "reallyname": "管理员",
}

# 子任务包所需要数据
TEST_DATA_WORKER = {
    "taskpackage_name": "task1",
    "user_username": "worker",
    "describe": "THIS IS DESCRIBE",
    "schedule": "一对多修改",
    "regiontask_name": "东南区域1800幅",
    "reallyname": "作业员",
}

# @所需要的数据
TEST_DATA_1 = {
    "taskpackage_name": "task11",
    "owner": "root",
    "owner2": "worker",
    "describe": "this is test_data",
    "regiontask_name": "东南区域1800幅"
}

# 进度所需数据
TEST_DATA_SCHEDULE = {
    "schedule":"测试进度",
    "regiontask_name":"东南区域1800幅"
}
TEST_LIST1_SCHEDULE = [
    "200", "修改缝隙", "河网环修改", "有向点修改", "一对多修改", "匝道赋值", "同层拓扑", "不同层拓扑", "微短线修改", "微小面修改", "急锐角修改"
]
TEST_LIST2_SCHEDULE = ["200", "等高线拼接", "完成"]


# 任务区域数据
TEST_DATA_REGIONSTAK = {
    "name":"测试区域",
    "describe":"this is test_data"
}


# 任务包页面排序后名字,默认数据task01~task20
ORDER_DATA_LIST1 = ["task{0}".format(num) for num in range(1, 11)]
ORDER_DATA_LIST2 = ["task{0}".format(num) for num in range(11, 21)]
ORDER_DATA_LIST3 = ["task{0}".format(num) for num in range(11, 16)]
ORDER_DATA_LIST4 = ["task{0}".format(num) for num in range(16, 21)]


# 通用执行sql函数
def clear(SQL):
    conn = psycopg2.connect(dbname="test",
                            user="postgres",
                            password="Lantucx2018",
                            host="192.168.3.120",
                            port="5432")
    cur = conn.cursor()
    cur.execute(SQL)
    conn.commit()
    conn.close()
