from common.read_excel import ReadExcel
from common.constant import DATA_DIR
from common.config import conf
from common.http_requests import HTTPRequest,HTTPRequest2
from common.logger import logger
from librarys.ddt import data,ddt
import os,unittest,random

# 配置文件中读取相关配置数据
filename = conf.get('excel', 'file_name')

# 随机生成手机号码
def rand_phone():
    phone = '134'
    for i in range(9):
        j = random.randint(0,9)
        phone += str(j)
    return phone

@ddt
class RegisterTestCase(unittest.TestCase):
    # 读取用例数据
    wb = ReadExcel(os.path.join(DATA_DIR,filename),'register')
    cases = wb.read_data_line_obj_new()

    @classmethod
    def setUpClass(cls):
        cls.request = HTTPRequest()
        cls.db = readmysql()

    @classmethod
    def tearDownClass(cls):
        logger.info("用例执行完毕")

    @data(*cases)
    def test_reister(self,case):
        # 你用例参数化
        # 注册：先去数据库查是否存在，存在则从新生成
        if "#reister_phone#" in case.data:
            # 替换测试的号码
            while True:
                phone = rand-phone()
                # 查询数据库该号码是否存在
                self.db.find_count("select * from meber where MobilePhone={}".format(phone))
                if count == 0:
                    break
            case.data.replace('#reister_phone#',phone)
        # 已经注册过的，从数据库获取张海波
        if "#phone#" in case.data:
            phone = self.db.find_one("select * from meber limit 1")[0]
            case.data.replace('#phone#', phone)
        # 充值取现之前需要登录加登录账号可配置再配置文件
        # 方法二、获取数据库最大值加1，或最新值减1



        # 发送请求获取结果
        response = self.request.request(method=case.method,url=case.url,data=eval(case.data))
        try:
            # 预期的结果case.excepted  实际结果response.text
            logger.info('预期结果：{},实际结果：{}'.format(case.excepted,response.text))
            self.assertEqual(case.excepted,response.text)
        except AssertionError as e:
            # 测试未通过，输出日志
            logger.error(e)
            # 在excel用例中写入结果
            self.wb.write_data(row=case.case_id+1,column=8,msg='failed')
            raise e
        else:
            # 测试通过，输出日志
            logger.info('测试用例：{}已通过'.format(case.title))
            # 在excel用例中写入结果
            self.wb.write_data(row=case.case_id+1,column=8,msg='pass')

@ddt
class LoginTestCase(unittest.TestCase):
    PASS



