from flask import  Flask
from flask import request,render_template


# 创建Flask对象-Httpd WEB服务对象

app = Flask('hiflask') # __name__可以是任意的小写字母，表示Flask应用对象的名称

#声明WEb服务的请求资源（指定资源访问的路由）
#RESTful 设计风格中关于资源的动作：'GET','POST','PUT','DELETE','PATCH'查询，更新，上传，删除，批量更新
@app.route('/hi', methods=['GET','POST'])
def hi():
    # from flask import request
    # request是请求对象（HttpRequest）,它包含请求资源的路径，请求方法，请求头，上传的表单数据，文件的等信息
    # 获取请求这种的查询参数(username,password):
    # wsgi -> QUERY_STRING:
    # query_string = 'username=disen&password=123'
    # args = {item.split('=')[0]:item.split('=')[1] for item in query_string.split('&')}
    # print(args)->{'username':'disen','password':'123'}
    # name = request.args.get('username')
    # password = request.args.get('password')

    #使用request请求获取请求方法
    # from flask import request

    # 获取平台参数：platform
    # 只支持Android手机访问
    platform = request.args.get('platform','pc')
    if platform.lower() != 'android':
        return """
            <h2>目前只支持Android设备 </h2>
        """

    if request.method == 'GET':
    #返回生成的HTMl网页内容(动态资源)
        return """
        <h1>用户登录的信息</h1>
        <form action="/hi?platform=android" method="post">
        <input name="name" placeholder="用户名"><br>
        <input name="pwd" placeholder="口令"><br>
        <button>提交</button>
        </form>
        """
    else:
        # 获取表单的参数
        name = request.form.get('name')
        pwd = request.form.get('pwd')
        if all((
            name.strip() == 'liyuanjie',
            pwd.strip() == '123'
        )):
            return """
                <h2 style="color:blue;">登录成功</h2>            
            """
        else:
            return """
                <h2 style="color:orange;">登陆失败，<a href="/hi?platform=android">重试</a></h2>
            """

@app.route('/bank',methods=['GET','POST'])
def addBank():
    # 练习：
    #1.GET请求返回添加银行卡的网页
    #2.post请求获取用户输入的信息，判断是否为空，为空是提示错误
    #  不为空提示添加成功且后台日志中显示

    # 加载数据（Model 交互操作）
    data = {
        'title': '绑定银行卡',
        'error_message': ''
    }
    if request.method == 'POST':
        name = request.form.get('name', None)
        card_num = request.form.get('card_num', None)
        if all((name,card_num)):
            # 使用flask的日志记录器(名称为当前的脚本名称)
            app.logger.info('name:%s->card:%s' % (name,card_num))
            return """
                <h2>绑定成功</h2>
                <h4 id="result"></h4>
                <script>
                    let steps = 5;
                    let interval_id = setInterval(()=>{
                        if(steps >=0) {
                            document.getElementById('result').innerText="剩余秒数" + steps-- + "秒"
                        }else{
                            // 取消定时器
                            clearInterval(interval_id)
                            window.open('/hi',target='_self')
                        }
                    },1000)
                </script>
            """

        data['error_message'] = '银行名称或账号不能为空'
    # 渲染模板
    return render_template('bank_edit.html',**data)
# 启动flask的WEB服务器
app.run('localhost',
        5000,
        True,  # 默认未开启调试模式，True开启调试模式
        threaded=True, #默认单线程，即为False
        processes=1) # 默认只有一个进程