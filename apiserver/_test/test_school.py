from unittest import TestCase

import requests


# 声明单元测试类
class TestSchool(TestCase):

    # 声明单元测试的方法
    # 方法名以"test_"开头
    def test_del(self):
        url = "http://localhost:5000/bank/del/1"
        # method = 'DELETE'
        # resp = requests.request(method, url)
        resp = requests.delete(url)
        # 断言，最后一个参数表示断言失败的信息
        self.assertIs(resp.status_code, 200, '请求失败')

        print(resp.text)

    def test_publish(self):
        url = "http://localhost:5000/bank/publish"
        resp = requests.post(url)
        self.assertEqual(resp.status_code, 200, '请求失败')
        print(resp.text)
        # 查看响应数据的类型
        print(resp.headers.get('Content-Type'))