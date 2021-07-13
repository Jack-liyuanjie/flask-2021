from unittest import TestCase
from models import db, User, Card, Bank
from mainapp import app


class TestRaw(TestCase):
    def test_user_data(self):
        sql = "select name,phone from user where name = '%s' limit 5"
        app.app_context().push()
        result = db.session.execute(sql % '李元杰')
        print(type(result.cursor))  # pymysql.cursors.Cursor
        # cursor对象也可以被迭代
        # for name, phone in result.cursor.fetchall():
        for name, phone in result.cursor:
            print(name, phone)

    def test_card_user_bank(self):
        # app.app_context().push()
        with app.app_context():
            sql = """
                select u.name, u.phone, b.name, b.address, c.number, c.money
                from user u
                join card c on (u.id = c.user_id)
                join bank b on (b.id = c.bank_id)
                order by c.money desc
            """
            exc = db.session.execute(sql)
            for username, phone, bankname, address, number, money in exc.cursor:
                print(username, phone, bankname, address, number, money)

    def test_user_card(self):
        app.app_context().push()
        result = db.session.query(User.name,
                                  User.phone,
                                  Bank.name.label('bankname'),
                                  Bank.address,
                                  Card.money,
                                  Card.number) \
            .filter(User.id == Card.user_id) \
            .filter(Bank.id == Card.bank_id)
        for item in result.all():
            print(item.name, item.phone, item.bankname, item.address,item.money, item.number)
