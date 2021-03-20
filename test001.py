from common.config import conf
from common.logger import logger

print(conf.get('excel','file_name'))
logger.info("--info--信息")