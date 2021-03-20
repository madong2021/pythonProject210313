import configparser
import os
from common.constant import CONF_DIR

class ReadConfig(configparser.ConfigParser):

    def __init__(self):
        super().__init__()
        # 加载文件
        r =configparser.ConfigParser()
        # 读取开关文件
        r.read(os.path.join(CONF_DIR,'env.ini'),encoding='utf-8')
        switch = r.get('env','switch')
        # 判断开关的值，选择加载环境的配置文件1开发环境0测试环境-
        if switch == '1':
            self.read(os.path.join(CONF_DIR,'config1.ini'),encoding='utf-8')
        else:
            self.read(os.path.join(CONF_DIR, 'config.ini'), encoding='utf-8')

conf = ReadConfig()

if __name__ == '__main__':
    res = conf.get('excel','file_name')
    print(res)