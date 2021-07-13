from unittest import TestCase
from mainapp import app
from models import db, User, Bank, Card


class TestRalationshap(TestCase):
    def test_1(self):
        app.app_context().push()
        user = User.query.get(1)
        print(type(user))
        for card in user.cards:
            print(card.bank.name, card.number, card.money, card.user.name)

    def test_2(self):
        app.app_context().push()

        for card in Card.query.all():
            # 显示用户名，用户手机号，银行名，存款
            print(card.user.name, card.user.phone, card.bank.name, card.money)
