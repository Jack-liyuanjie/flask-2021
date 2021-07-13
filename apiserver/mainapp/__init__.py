import math

from flask import Flask, render_template
from flask_session import Session
from models import db

import settings
app = Flask(__name__)

# 从指定对象中加载Flask服务的配置
app.config.from_object(settings.Dev)
# 设置secret_key
app.config['SECRET_KEY'] = 'lingua'


session = Session()
session.init_app(app)

# 初始化sqlalchemy类对象
db.init_app(app)

# @app.errorhandler(404)
# def notfound(error):
#     print(error)
#     return render_template('404.html')
#
#
# @app.errorhandler(Exception)
# def handlerOfError(error):
#     return render_template('500.html')


# 自定义模板过滤器
@app.template_filter('datefmt')
def datefmt_filter(value, *args):
    print(value,type(value),args)
    # value是datetime类型
    # Python的自省函数
    # isinstance(),issubcalss()
    # hasattr(),getattr(),setattr()
    # dir(),type()
    return value.strftime(args[0])

@app.template_filter('moneyfmt')
def moneyfmt_filter(value,method="common",precision=0):
    # 'common'普通的金额格式化
    value = round(value,precision)
    if method == 'common':
        # 以千位符分割
        if isinstance(value,int):
            pre_v=str(value)
            end_v=''
        else:
            pre_v,end_v = str(value).split('.')
            end_v = "."+end_v
        pre_v = pre_v[::-1]

        vs = [pre_v[i*3: i*3+3] for i in range(math.ceil(len(pre_v)/3))]
        return ','.join(vs)[::-1] + end_v

    # 'currency' 货币单位，万，百万，千万，亿
    cur = ''
    if value / 10000 < 1:
        cur = ' 元'
    elif value / (100*1000) < 1:
        cur = '万元'
        value = round(value / 10000, 2)
    elif value / (1000*10000) < 1:
        cur = '百万'
        value = round(value / (100*10000), 2)
    elif value / (10000*10000) < 1:
        cur = '千万'
        value = round(value / (1000*10000), 2)
    else:
        cur = '亿元'
        value = round(value / (10000 * 10000), 2)
    return str(value)+cur
