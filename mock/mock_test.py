import requests
from unittest import mock
url = 'http://182.254.200.120:8123/login'
data = {'user':'python01','pwd':123456}
# {'code':1,'msg':'登录成功'}
# requests.post(url,data=data)
m1 = mock.Mock(return_value={'code':1,'msg':'登录成功'})
res = m1(url,data=data)
print(res)