import random

from help import crypy
from unittest import TestCase
from mainapp import app
from models import db, User, Card, Bank


class TestUser(TestCase):
    def test_query(self):
        # 获取falsk服务的上下文环境
        # SQLAlchemy的数据库连接环境时Flask运行的基础
        with app.app_context():
            users = User.query.all()
            for u in users:
                print(u.name, u.id)

    def test_create(self):  # 增加
        app.app_context().push()  # 向栈推上下文
        # User = user()
        # User.name = '亚索'
        # User.phone = '1111111111'
        # User.number = '46786289337927830'
        # User.password = crypy.pwd('1234')
        user = User(name='万豪',
                    number='6786456989758776647',
                    phone='269542558',
                    password=crypy.pwd('678954'))

        db.session.add(user)
        db.session.commit()  # 提交事务

    def test_update(self):  # 更新
        app.app_context().push()
        user = User.query.get(5)
        print(user)

        user.name = '疾风剑豪'
        user.phone = '6666'

        db.session.commit()  # 自动检查数据是否发生变化，如果发生变化自动更新

    def test_delete(self):  # 删除
        app.app_context().push()
        db.session.delete(User.query.get(6))
        db.session.commit()

    def test_filter(self):
        app.app_context().push()
        # 查询所有x姓名中包含“李”字的用户
        for u in User.query.filter(User.name.contains('李')):
            print(u)
        # 查李开头的
        for u in User.query.filter(User.name.startswith('李')):
            print(u)
        # 查李元杰
        for u in User.query.filter(User.name == '李元杰'):
            print(u)

        # 查询取一条记录one()读取一个，all()读取多个
        u = User.query.filter(User.number == '431121199709098771').one()
        print(u)

        # 验证登录
        filter = User.query.filter(User.name == '李元杰',
                                   User.password == '123456')

        try:
            login_user = filter.one()
            print(login_user, '登陆成功')
        except:
            print('账号或者口令错误')

    def test_filter_no_or(self):
        app.app_context().push()
        # 查询id大于等于4或者名字包含西安的银行
        for b in Bank.query.filter(db.or_(
                Bank.id >= 3,
                Bank.name.like('%西安%')
        )):
            print(b.id, b.name, b.address)

        # 查询非“西安”的银行
        for b in Bank.query.filter(db.not_(Bank.name.contains('西安'))):
            print(b.id, b.name, b.address)

    def test_filter_func(self):
        app.app_context().push()
        # 查询余额大于等于400000的银行卡__ge__() 相当于>=,__le__()相当与<=
        for c in Card.query.filter(Card.money.__ge__(400000)):
            print(c.number, c.money)

    def test_session_query(self):
        app.app_context().push()

        # 查询用户的手机号和身份证号
        # first() 也可以使用all()
        u = db.session.query(User.number, User.phone).first()
        print(u.number, u.phone)
        u = db.session.query(User.number, User.phone).all()
        print(u[0].number, u[0].phone)

        # session的query必须要指定模型才可以查询
        for u in db.session.query(User).all():
            print(u.name, u.phone)

    def test_model_query(self):
        app.app_context().push()
        # 模型类的query是BaseQuery类对象，不可以被调用
        # 以下代码错误
        for u in User.query(User.name, User.phone).all():
            print(u.name, u.phone)

    def test_model_order(self):
        app.app_context().push()

        # 按身份证排序
        # 先按姓名排序，姓名相同，再按身份证排序
        # 默认按升序ASC->asc()，可以指定降序DESC->desc()
        for u in User.query.order_by(User.name, User.number.desc()):
            print(u.name, u.phone)
        print('------------------------------------------------------------')
        for u in User.query \
                .filter(User.name.startswith('叶')) \
                .order_by(User.phone.desc()).all():
            print(u.name, u.phone, u.number)

        # 查询余额按降序排序
        for c in db.session.query(Card).order_by(Card.money.desc()).all():
            print(c.money, c.bankname, c.username)

    def test_page(self):
        app.app_context().push()

        # 一页显示2人
        # total = user.query.count()
        # page_size = 2
        # pages = total // page_size + (1 if total % page_size > 0 else 0)
        # print(total)
        # print('总条数：%s，每页显示 %s 条，总页数: %s' % (total, page_size, pages))
        # page = random.randint(1, pages)
        # print('现在是第%s页' % page)
        # for u in user.query.order_by(user.id).offset((page - 1) * page_size).limit(page_size).all():
        #     print(u.name, u.phone)

        # 查13或者23开头的手机号的用户信息
        # 先按照手机号排序在分页
        query_set = User.query.filter(db.or_(
            User.phone.startswith('13'),
            User.phone.startswith('23')
        )).order_by(User.phone);
        for u in self.page_data(query_set, page=3).all():
            print(u.name, u.phone)

    def page_data(self, query_set, page_size=2, page=1):
        total = query_set.count()
        pages = total // page_size + (1 if total % page_size > 0 else 0)
        print('总条数：%s,每页显示%s条，总页数:%s' % (total, page_size, pages))
        if page > pages:
            page = pages
        elif page <= 0:
            page = 1
        print('-------显示第 %s 页--------' % page)
        return query_set.offset((page - 1) * page_size).limit(page_size)

    def test_aggr(self):
        app.app_context().push()
        cnt = db.session.query(db.func.count(User.id)).first()
        print(cnt)

        # 统计的字段可以使用.label()设置别名
        # 除统计之外的字段需要放在group_by()分组语句中
        # 对.able()别名的字段排序，可以使用db.Column()转换再使用desc()或者asc()
        # 聚合后的查询结果的每一个元素是元组类型，不是模型对象
        result = db.session.query(User.name, db.func.count(User.id).label('cnt')).group_by(User.name).order_by(
            db.column('cnt').desc()).all()
        for u in result:
            print(u)

    def test_sum_money(self):
        app.app_context().push()
        # 查询每个人的财富
        result = db.session.query(Card.user_id,
                                  db.func.sum(Card.money).label('total')) \
            .group_by(Card.user_id) \
            .having(db.Column('total').__ge__(40000)) \
            .order_by(db.Column('total').desc()).all()

        print(result)

        # 二次查询
        user_totals = [(User.query.get(user_id), money) for user_id, money in result]
        for user_total, money in user_totals:
            print(user_total.name, money)

        for user_id, money in result:
            print(User.query.get(user_id).name, money)

    def test_bank_money(self):
        app.app_context().push()
        # 汇总每个银行的开户人数，总金额，和每个银行的最小金额和最大金额银行卡绑定的用户信息
        # result1 = db.session.query(Card.bank_id,
        #                            db.func.count(Card.user_id).label('um')) \
        #     .group_by(Card.bank_id) \
        #     .order_by(db.Column('um').desc()).all()
        # t = []
        # for bank_id, n in result1:
        #     t.append(bank.query.get(bank_id).name)
        #     t.append(n)
        # print(t)
        #     # print(bank.query.get(bank_id).name, n)
        # --------------------------------------------------------------------------------------------------------------
        # result2 = db.session.query(Card.bank_id,
        #                            db.func.sum(Card.money).label('mm')) \
        #     .group_by(Card.bank_id) \
        #     .order_by(db.Column('mm').desc()).all()
        # for bank_id, m in result2:
        #     print(bank.query.get(bank_id).name, m)
        # --------------------------------------------------------------------------------------------------------------
        # result4 = db.session.query(user.id, user.name).all()
        # print(type(result4[0]))  # <class 'sqlalchemy.engine.row.Row'>
        # for u in result4:
        #     print(u.id, u.name)

        # for id,name in result4:
        #     print(id,name)
        result1 = db.session.query(Card.bank_id,
                                   db.func.max(Card.money).label('max'),
                                   db.func.min(Card.money).label('min'),
                                   db.func.count(Card.user_id).label('um'),
                                   db.func.sum(Card.money).label('cm')) \
            .group_by(Card.bank_id).all()
        print(result1)
        for i in result1:
            print(Bank.query.get(i.bank_id).name, i.um, i.cm, i.min, i.max)
            print('----------最小和最大的存款用户信息---------')
            for user_id, money in db.session.query(Card.user_id, Card.money) \
                                            .filter(Card.bank_id == i.bank_id,
                                                    db.or_(
                                                        Card.money == i.min,
                                                        Card.money == i.max
                                                    )).all():
                print(user.query.get(user_id).name, money)
