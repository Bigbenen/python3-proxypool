'''
页面获取基本函数
'''
import requests

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
}

def get_page(url):
    '''
    获取代理页面
    :param url:
    :param option:其他要添加的请求头，传入时需要字典格式
    :return: 代理页面响应
    '''
    headers = dict(base_headers)
    session = requests.Session()
    try:
        response = session.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError as e:
        print('页面抓取失败 ',e.args)
        return None