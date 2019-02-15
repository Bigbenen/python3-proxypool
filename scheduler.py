'''
调度模块，调用代理池的获取/检测/接口模块
'''

import time
from multiprocessing import Process

from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.setting import *


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        '''
        定时测试代理
        :param cycle:每隔多久测一次
        '''
        tester = Tester()
        while 1:
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        '''定时从网络获取代理'''
        getter = Getter()
        while 1:
            try:
                getter.run()
            except Exception as e:
                print('获取器错误', e.args)
            time.sleep(cycle)

    def schedule_api(self):
        '''开启api'''
        #app是一个方法？？类？
        app.run(API_HOST,API_PORT)

    def run(self):
        '''
        运行入口
        '''
        print('代理池开始运行')
        if GETTER_ENABLED == True:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if TESTER_ENABLED == True:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if API_ENABLED == True:
            api_process = Process(target=self.schedule_api)
            api_process.start()

if __name__=='__main__':
    scheduler = Scheduler()
    scheduler.run()