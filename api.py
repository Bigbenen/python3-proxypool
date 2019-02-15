'''
代理池网页接口模块
http://localhost:5000/random
'''
from proxypool.db import RedisClient
from flask import Flask,g

#不清楚该用法，为什么不构建一个app类??？把get_conn获取连接放入对象初始化中？def __init__(self)
__all__  = ['app']
app = Flask(__name__)

def get_conn():
    '''
    获取数据库连接
    :return: 数据库连接
    '''
    if not hasattr(g,'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool</h2>'

@app.route('/random')
def get_proxy():
    '''
    随机获取可用代理
    :return: 代理
    '''
    conn = get_conn()
    #print(type(conn.random()))
    return conn.random()

@app.route('/count')
def get_counts():
    '''
    获取代理池总量
    :return: 代理池总量
    '''
    conn = get_conn()
    #把结果转换为str类型，否则flask模块会报错
    return str(conn.count())

if __name__=='__main__':
    app.run()
