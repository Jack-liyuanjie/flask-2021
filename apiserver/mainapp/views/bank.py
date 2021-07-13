from flask import Blueprint, make_response, Response, render_template, redirect, url_for, abort
from flask import request, jsonify
from dao import bank_dao
from dao.bank_dao import BankDao

blue = Blueprint('bankBlue', __name__)


@blue.route('/add', methods=['GET', 'POST'])
def addCard():
    if request.method == 'POST':
        # 接收开户信息
        bankId = request.form.get('bank')
        username = request.form.get('username')
        phone = request.form.get('phone')

        if phone == '13267886101':
            # 终端业务
            abort(Response("<h3 style='color:red'>%s 当前手机号不能被注册</h3>" % phone), 403)
        # 验证是否为空
        # 假如操作成功
        # 进入列表页面
        return redirect(url_for('bankBlue.listCard'))
    # GET请求响应开户页面
    return render_template('card/add.html')


@blue.route('/list2')
def listCard():
    from models import bank
    data = {
        'banks': bank.query.all()
    }
    return render_template('bank/list2.html',**data)


@blue.route('/publish', methods=['POST'])
def publish_bank():
    data = "预发布银行公告"
    code = 200
    # 将数据和状态码封装到响应对象中
    response = Response(data, code, content_type="application/json")
    return response


@blue.route('/findbank', methods=['GET', 'POST'])
def bank():
    dao = bank_dao.BankDao()
    data = dao.find_all()  # list[{},....]
    return jsonify({
        'status': 20,
        'message': 'find all ok',
        'data': data
    })


@blue.route('/edit/<int:bankId>', methods=['GET'])
def edit(bankId):
    return "正在编辑：银行编号 %s" % bankId


@blue.route('/del/<int:bank_id>', methods=['DELETE'])
def del_bank(bank_id):
    return "<h3>正在删除银行：%s</h3>" % bank_id


@blue.route('/find/<keyword>', methods=['GET'])
def find(keyword):
    # keyword可能时名称，id，网站
    return "keyword是%s类型，值是%s" % (type(keyword), keyword)


@blue.route('/forword/<path:url>', methods=['GET'])
def forword(url):
    return """
        <h4 id="result"></h4>
        <script>
            let steps = 5;
            let interval_id = setInterval(()=>{
                if(steps >=0) {
                    document.getElementById("result").innerText="剩余秒数" + steps-- + "秒"
                }else{
                    clearInterval(interval_id)
                    window.open("%s",target="_self")
                }
            },1000)
        </script>    
    """ % url
