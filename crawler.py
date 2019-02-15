import json
from proxypool.utils import get_page
import bs4
from bs4 import BeautifulSoup
import lxml
#后续优化为xpath
from lxml import etree

class ProxyMetaclass(type):
    # 通过元编程，动态获取Crawler类中的命名空间，收集所有以crawl_开头的方法放入__CrawlFunc__属性中，在getter.run方法中遍历调用
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count +=1
        attrs['__CrawlFuncCount__'] = count
        #print('!!',attrs['__CrawlFunc__'])
        return type.__new__(cls, name, bases, attrs)

class Crawler(object,metaclass=ProxyMetaclass):
    #def __init__(self):
        #self.test =1
        #print(self.__dict__)
    #！！！元类.__new__()的attrs可以获得类的命名空间，测试发现可以获得x
    #但不会获得selef.test，其包含在__init__内，是类的实例的属性
    #x = 2
    def get_proxies(self,callback):
        print('获取器执行方法：{}'.format(callback))
        proxies = []
        try:
            for proxy in eval("self.{}()".format(callback)):
                proxies.append(proxy)
            print('{} 成功获取到代理-列表：{}'.format(callback, proxies))
        except Exception as e:
            print('获取器方法<{}>发生错误,{}'.format(callback, e.args))
        return proxies

    def _daili66(self,page_count=5):
        '''
        获取66ip代理
        :param page_count:页码
        :return: 代理
        '''
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            #print('crawling ', url)
            html = get_page(url)
            # print('##html',html)
            soup = BeautifulSoup(html, 'lxml')
            #print('##soup', soup)
            trs = soup.select('.containerbox.boxindex table tr')[0].find_all_next('tr')
            for tr in trs:
                ip = tr.select('td')[0].text
                # next_sibling得到的不一定是Tag类型，也可能是字符串！
                port = tr.select('td')[1].text
                yield ':'.join([ip, port])


    def _goubanjia(self):
        '''
        获取Goubanjia代理
        :return: 代理
        '''
        start_url = 'http://www.goubanjia.com'
        #print('crawling ',start_url)
        html = get_page(start_url)
        soup = BeautifulSoup(html,'lxml')
        tds = soup.select('td.ip')
        for td in tds:
            ips = td.contents
            #据观察，相邻元素的text文本不能相同，有重复的则跳过
            qc = ''
            ip_string = ''
            for ip in ips:
                if isinstance(ip,bs4.element.Tag):
                    if ip.text != qc:
                        qc = ip.text
                        ip_string += qc
                else:
                    #非tag类型则为':'
                    ip_string +=ip
            yield ip_string

    def crawl_wanglian(self):
        API = 'http://47.96.139.87:8081/Index-generate_api_url.html?packid=1&fa=0&qty=1&port=1&format=txt&ss=1&css=&pro=&city='
        html = get_page(API)
        if html is not None:
            soup = BeautifulSoup(html, 'lxml')
            ips = soup.select('p')[0].get_text().split()
            for ip in ips:
                # print('获取到',ip)
                yield ip
