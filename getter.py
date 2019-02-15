from proxypool.crawler import Crawler
from proxypool.db import RedisClient
from proxypool.setting import *


class Getter():
    def __init__(self):
        self.crawler = Crawler()
        #print(self.crawler.__dict__)
        self.redis = RedisClient()

    def is_over_threshold(self):
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行')
        #print(self.crawler.__CrawlFunc__)
        if not self.is_over_threshold():
            for callback in self.crawler.__CrawlFunc__:
                # 每次调用得到一个代理ip列表
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)
        else:
            print('代理池已满，不会获取新的代理')

if __name__=='__main__':
    getter = Getter()
    getter.run()
