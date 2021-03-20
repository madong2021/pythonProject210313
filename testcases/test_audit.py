from common.read_excel import ReadExcel
from common.constant import DATA_DIR
from common.config import conf
from common.http_requests import HTTPRequest,HTTPRequest2
from common.logger import logger
from librarys.ddt import data,ddt
import os,unittest,random
from common.replace import replace,ConText


@ddt
class AuditTestCase(unittest.TestCase):
    # 读取用例数据
    wb = ReadExcel(os.path.join(DATA_DIR,filename),'audit')
    cases = wb.read_data_line_obj_new()

    @classmethod
    def setUpClass(cls):
        logger.info("用例开始执行")
        cls.request = HTTPRequest()
        cls.db = readmysql()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        cls.request.close()
        logger.info("用例执行完毕")

    @data(*cases)
    def test_audit(self,case):
        # 准备数据
        url = conf.get('env','url')+case.url
        case.data = replace(case.data)

        # 测试用例中有*mloanId*需要替换，用例为标的为不存在
        sql = "select max(id) from member;"
        if "*loanId*" in case.data:
            # 获取数据库中最大的标id进行加一，然后进行替换
            memberId = self.db.find_one(sql)[0]
            memberId += 1
            # 替换
            case.data = case.data.replace("*loanId*",str(loanId))

        # 发送请求获取结果
        response = self.request.request(method=case.method,url=url,data=eval(case.data))
        code = response.json()['code']

        if response.json()['msg'] == "加标成功":
            sql = "select id from loan where memberId=#memberId# order by id desc limit 1;"
            replace(sql)
            loan_id = self.db.find_one(sql)
            setattr(ConText,"loan_id",str(loan_id))

        # 对比结果
        try:
            self.assertEqual(str(case.excepted),code)

            # 获取加标后标的数量
            if case.check_sql:
                # 获取加标前的标数量
                case.check_sql = replace(case.check_sql)
                status = self.db.find_count(case.check_sql)
                self.assertEqual(eval(case.data)['status'],status)

        except AssertionError as e:
            # 测试未通过，输出日志
            logger.error(e)
            # 在excel用例中写入结果
            self.wb.write_data(row=case.case_id+1, column=9, msg=response.text)
            self.wb.write_data(row=case.case_id+1,column=8,msg='failed')
            raise e
        else:
            self.wb.write_data(row=case.case_id+1, column=9, msg=response.text)
            # 在excel用例中写入结果
            self.wb.write_data(row=case.case_id+1,column=8,msg='pass')
