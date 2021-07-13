from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    # 声明字段（属性），默认情况下属性名与字段相同
    # uid = db.Column('id', primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50))
    password = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return "%s %s" % (self.name, self.number)


class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String(50), unique=True)
    money = db.Column(db.Float(2), default=0, server_default='0')
    password = db.Column(db.String(50))

    # 模型的关系维护（建立）在多端
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, backref=db.backref('cards', lazy=True))
    # user = db.relationship(User, backref='cards')

    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'))
    # bank = db.relationship(Bank, backref='cards')
    # lazy表示关联的数据是否延迟加载，为False时使用join关联查询
    bank = db.relationship(Bank, backref=db.backref('cards', lazy=True))

    # user_id = db.Column(db.Integer)
    # bank_id = db.Column(db.Integer)
    #
    # @property
    # def username(self):
    #     return user.query.filter(user.id == self.user_id).all()[0].name
    #
    # @property
    # def bankname(self):
    #     return bank.query.filter_by(id=self.bank_id).all()[0].name
