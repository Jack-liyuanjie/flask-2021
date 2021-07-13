from flask import Blueprint, render_template
from flask import url_for

from dao.card_dao import CardDao

blue = Blueprint('cardBlue', __name__)


@blue.route('/add/<bankName>/<int:page>')
def addCard(bankName, page):
    return """
        %s 开户成功！目前在第%s页
        <br>
        <a href="%s">返回首页</a>
    """ % (bankName, page, url_for('index'))


@blue.route('/select_bank')
def seletBank():
    # 查询所有银行，供用户选择
    # 用户选择之后，进入开户页面
    bankName = "中国银行"
    # next_url = "/card/add/" + bankName
    return """
    选择银行成功，3秒后<a href="%s">进入开户页面</a>
    """ % url_for('cardBlue.addCard', bankName=bankName, page=1)


@blue.route('/list2')
def list4db():
    # dao = CardDao()
    from models import Card
    data = {
        'card': Card.query.all()
    }
    return render_template('card/list2.html', **data)

