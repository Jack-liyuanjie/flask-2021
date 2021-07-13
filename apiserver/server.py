from flask import url_for, render_template

from mainapp import app
from mainapp.views import bank, card, user
from flask_script import Manager
from flask_cors import CORS


@app.route('/')
def index():
    data = {
        'menus': ['用户管理','订单管理','地址管理']
    }
    return render_template('index.html', **data)
    # return """
    #     <ul>
    #         <li> <a href="%s">银行卡开户</a></li>
    #         <li> <a href="%s">银行卡管理</a></li>
    #         <li> <a href="%s">用户管理</a></li>
    #     </ul>
    # """ % (
    #     url_for('cardBlue.addCard', bankName='中国银行', page=1),
    #     url_for('bankBlue.edit', bankId=1),
    #     url_for('userBlue.find')
    # )


if __name__ == '__main__':
    # 跨域访问
    CORS().init_app(app)

    # 将蓝图对象注册到flask服务中
    # 在注册蓝图对象时可以加路由访问的前缀url_prefix='前缀名'访问时先加前缀名再加路由名
    app.register_blueprint(bank.blue, url_prefix='/bank')
    app.register_blueprint(user.blue, url_prefix='/user')
    app.register_blueprint(card.blue, url_prefix='/card')
    # 以脚本的方式启动flask应用服务
    manager = Manager(app)
    manager.run()
