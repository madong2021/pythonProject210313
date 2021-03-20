from common.read_excel import ReadExcel
from common.constant import DATA_DIR
from common.config import conf
from common.http_requests import HTTPRequest,HTTPRequest2
from common.logger import logger
from librarys.ddt import data,ddt
from common.do_mysql import ReadMysqlData
import os,unittest

# 配置文件中读取相关配置数据
filename = conf.get('excel', 'file_name')

@ddt
class RechargeTestCase(unittest.TestCase):
    """充值和提现接口"""
    wb = ReadExcel(os.path.join(DATA_DIR,filename),'recharge')
    cases = wb.read_data_line_obj_new()

    @classmethod
    def setUpClass(cls):
        logger.info("用例开始执行")
        cls.request = HTTPRequest2()
        cls.db = ReadMysqlData()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        cls.request.close()
        logger.info("用例执行完毕")

    @data(*cases)
    def test_recharge_withdraw(self,case):
        # 判断该条测试数据是否有sql语句
        if case.check_sql:
            s_money = self.db.find_one(case.check_sql)[0]
        # 发送请求获取结果
        url = conf.get('env','url')+case.url
        print(case.data)
        response = self.request.request(method=case.method,url=url,data=eval(case.data))
        try:
            # 校验预期结果
            # 预期的结果case.excepted  实际结果response.json()['code']
            self.assertEqual(case.excepted,response.json()['code'])
            # 校验结果码
            if case.check_sql:
                # 执行sql语句，获取余额
                e_money = self.db.find_one(case.check_sql)[0]
                # 本次充值金额
                money = eval(case.data)['amount']
                # 判断是充值接口还是取现接口
                if case.interface == "充值":
                    logger.info('充值前金额{}，充值后金额{}，本次充值金额{}'.format(s_money,e_money,money))
                    self.assertEqual(e_money-s_money, money)
                else:
                    logger.info('取现前金额{}，取现后金额{}，本次取现金额{}'.format(s_money,e_money,money))
                    self.assertEqual(s_money-e_money, money)
        except AssertionError as e:
            # 测试未通过，输出日志
            logger.error(e)
            # 在excel用例中写入结果
            self.wb.write_data(row=case.case_id+1,column=10,msg='failed')
            self.wb.write_data(row=case.case_id+1, column=9, msg=response.text)
            raise e
        else:
            # 测试通过，输出日志
            logger.info('测试用例：{}已通过'.format(case.title))
            # 在excel用例中写入结果
            self.wb.write_data(row=case.case_id+1,column=10,msg='pass')
            self.wb.write_data(row=case.case_id+1, column=9, msg=response.text)
