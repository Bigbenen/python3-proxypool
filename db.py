'''
代理池存取模块，基于redis库；
是最基本的模块，用于支持代理池其他三个模块：获取模块/检测模块/接口模块。
'''
# 有Redis和StrictRedis两个类，官方推荐使用后者
from redis import StrictRedis
import re
from random import choice
from proxypool.error import PoolEmptyError
from proxypool.setting import *


class RedisClient():
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        '''
        初始化，使每个RedisClient对象能连接到redis数据库
        :param host: redis地址
        :param port: redis端口
        :param password: 密码
        '''
        self.db = StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        '''
        添加代理，设置其分数为初始值
        :param proxy: 代理
        :param score: 初始分
        #不需要返回添加结果吧！
        #:return: 添加结果，返回的是添加的元素个数
        '''
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            self.db.zadd(REDIS_KEY, score, proxy)

    def decrease(self,proxy):
        '''
        代理的分数减一分，分数低于最小值则删除代理
        :param proxy: 代理
        #:return: 修改后的代理分数
        '''
        score = self.db.zscore(REDIS_KEY, proxy)
        #此判断条件可优化，因为假如MIN_SCORE小于0时逻辑就错了
        if score and score > MIN_SCORE:
            self.db.zincrby(REDIS_KEY, proxy, -5)
            #print('代理暂时不可用 ', proxy, '当前分数 ', score, '减 5')
        else:
            self.db.zrem(REDIS_KEY, proxy)
            #print('代理完全不可用 ', proxy, '当前分数 ', score, '移除')

    def exists(self, proxy):
        '''
        判断代理是否存在
        :param proxy: 代理
        :return: 是否存在
        '''
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        '''
        将代理设置为MAX_SCORE
        :param proxy: 代理
        #:return: 设置结果
        '''
        self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)
        print('代理 ', proxy, '可用，设置为', MAX_SCORE)

    def count(self):
        '''
        获取代理数量
        :return: 数量
        '''
        return self.db.zcard(REDIS_KEY)

    def all(self):
        '''
        获取全部代理
        :return: 全部代理列表
        '''
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def random(self):
        '''
        随机获取可用代理，首先尝试最高分代理，如果无最高分代理，则按照排名获取
        :return:
        '''
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        print('满分代理', len(result), '个')
        print(result)
        if result:
            return choice(result)
        else:
            #zrevrange方法会按分数进行排名，若无满分代理，选择排名前50的代理
            result = self.db.zrevrange(REDIS_KEY, 0, 50)
            if result:
                print('使用第二梯队代理')
                return choice(result)
            else:
                raise PoolEmptyError

    def batch(self, start, stop):
        '''
        批量获得区间内的代理
        :param start: 起
        :param stop:终
        :return: 代理
        '''
        #stop减不减1都能正常运行，为保持每次获得100个，这里减1
        return self.db.zrevrange(REDIS_KEY, start, stop-1)
