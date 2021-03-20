import logging
from common.config import conf
import os
from common.constant import LOG_DIR

# 读取配置文件相关参数
logger_name = conf.get('logs', 'logger_name')
lever = conf.get('logs', 'lever').upper()
sh_lever = conf.get('logs', 'sh_lever').upper()
fh_lever = conf.get('logs', 'fh_lever').upper()
log_file_path = conf.get('logs', 'log_file_path')
log_file = os.path.join(LOG_DIR,log_file_path)
print(log_file)


class MyLogging(object):
    """自定义日志类"""

    def __new__(cls, *args, **kwargs):
        # 创建自己的日志收集器
        my_log = logging.getLogger(logger_name)
        my_log.setLevel(lever)
        # 创建一个日志输出渠道
        l_s = logging.StreamHandler()
        l_s.setLevel(sh_lever)
        # 将日志输出渠添加到日志收集器中
        l_f = logging.FileHandler(log_file, encoding='utf8')
        l_f.setLevel(fh_lever)
        # 把创建的渠道添加到收集器中
        my_log.addHandler(l_s)
        my_log.addHandler(l_f)
        # 设置日志的输出格式
        formart = '%(asctime)s-[%(filename)s-->line:%(lineno)d]-%(levelname)s:%(message)s'
        ft = logging.Formatter(formart)
        # 设置输出日志格式
        l_f.setFormatter(ft)
        l_s.setFormatter(ft)
        return my_log

logger = MyLogging()

if __name__ == '__main__':

    logger.info("haode")
