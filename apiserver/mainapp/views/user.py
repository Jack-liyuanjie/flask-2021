from flask import Blueprint, render_template, request, make_response, session, redirect
from datetime import datetime

# 创建蓝图的时候，第一个参数：name可以任意命名
# 第二个参数必须使用__name__表示导包名称
import dao
from dao.user_dao import UserDao

blue = Blueprint('userBlue', __name__)


@blue.route('/find', methods=['GET', 'POST'])
def find():
    return render_template("user/list.html", request=request)


@blue.route('/login2')
def login():
    response = make_response("进入登陆页面")
    # 添加cookie
    # expire_datetime = datetime.strptime('2021-6-19 3:40:00','%Y-%m-%d %H:%M:%S')
    # response.set_cookie('username','disen',expires=expire_datetime)
    # response.set_cookie('email','2311485953@qq.com',max_age=1209600)
    # 删除cookie
    # response.delete_cookie('email')
    return response


@blue.route('/login', methods=['GET', 'POST'])
def LoginUser():
    if request.method == 'POST':
        # 读取登录用户信息
        # 前端页面表单域：name,password
        name = request.form.get('name')
        password = request.form.get('password')
        if not all((name, password)):  # 验证是否为空
            message = "用户名或者口令不能为空"
        else:
            # 将数据写入数据库
            dao = UserDao()
            # dao.save(name=name,password=password) 注册时使用
            user = dao.login(name, password)  # 如果存在此用户，则返回用户用户信息，dict
            if not user:
                message = "查无 %s 此用户，请确认用户名或口令是否正确！" % name
            else:
                # 将用户信息
                session['login_user'] = user

                # 重定向到主页
                return redirect('/')
    context = locals()
    return render_template('user/login.html', **context)


@blue.route('/list')
def listUser():
    data = {
        "message": 'hello,template!',
        "age": 20,
        "birthday": datetime.now(),
        "money": 19000000.7657,
        "cate": ["财务", "会计", "财务", "会计", "老板", "老板"],
        "script": """
            <script>
                setTimeout(()=>{
                    document.write("haha")
                }, 1000)    
            </script>
        """,
        "level": "大神"
    }
    # **data => (message='hello,template!', age=20)
    return render_template('user/list.html', **data)


@blue.route('/list2')
def list4db():
    if not session.get('menus'):
        session['menus'] = [
            {'title': '用户管理', 'url': '/user/list2'},
            {'title': '银行管理', 'url': '/bank/list2'},
            {'title': '银行卡管理', 'url': '/card/list2'}
        ]
    from models import User
    # dao = UserDao()
    data = {
        'user': User.query.all(),
        'session': session
    }
    return render_template('user/list2.html', **data)
