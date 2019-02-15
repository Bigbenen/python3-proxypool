'''
代理有效性检测模块，使用协程/aiohttp库异步请求
'''
import asyncio
import sys
import time
import aiohttp
from proxypool.db import RedisClient
from proxypool.setting import *


class Tester():
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        '''
        测试单个代理
        :param proxy:
        :return:
        '''
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                #如果确保抓取/存入数据库的代理都是字符串格式，可以不要此判断；且改变类型后，调用redis.max方法后会"复制"一个代理。
                #if isinstance(proxy, bytes):
                    #proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                #print('正在测试 ', real_proxy, TEST_URL)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=10) as response:
                    #若代理可用，将分值设置为最高分
                    if response.status in VALID_STATUS_CODE:
                        self.redis.max(proxy)
                    else:
                        self.redis.decrease(proxy)
            except (aiohttp.ClientProxyConnectionError, aiohttp.ClientError, asyncio.TimeoutError, AttributeError) as e:
                #print('代理测试请求失败', proxy)
                self.redis.decrease(proxy)

    def run(self):
        '''
        测试主函数
        '''
        print('测试器开始运行，测试url ',TEST_URL)
        try:
            count = self.redis.count()
            print('当前有', count,'个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i+BATCH_TEST_SIZE,count)
                print('\n正在测试第{}到{}个代理'.format(start, stop))
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))

                result = self.redis.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
                print('满分代理', len(result), '个')

                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('测试器发生故障', e.args)

if __name__=='__main__':
    tester = Tester()
    tester.run()