import requests
from proxypool.setting import API_HOST,API_PORT


PROXY_POOL_URL = 'http://{}:{}/random'.format(API_HOST,API_PORT)

def get_ip():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError:
        #print('代理池连接异常')
        raise requests.ConnectionError('代理池连接异常')
        #return None

proxy = get_ip()
if proxy is not None:
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    }
    print('成功从代理池获取ip并合成:', proxies)

    url = 'http://httpbin.org/get'
    try:
        res = requests.get(url, proxies=proxies, timeout=5)
        # print(res.text)
        # print(type(res.json()))
        print(res.json().get('origin'))
        print(res.json())
    except Exception as e:
        print('Error', e.args, e.__traceback__)
else:
    print('从代理池获取ip失败，但与代理池连接无异常，请检查代理池运行状况！')