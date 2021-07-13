class User:
    id = 432212299709098770
    name = 'liyuanjie'
    phone = 13267886101
    money = 2000000


class Order:
    price = 4000
    number = 1001
    title = '华为牛逼'


def save(entity):
    print(dir(entity))
    # 读取对象的普通属性
    print([attr for attr in dir(entity) if not attr.startswith('__')])
    print(entity.__dict__)
    print({attr: getattr(entity, attr) for attr in dir(entity) if not attr.startswith('__')})

    # sql语句选择表插入值
    sql = "insert into %s(%s) values(%s)"
    # 创建具体表的变量
    table = entity.__class__.__name__.lower()
    # 创建表中key的值
    colname = ','.join([col for col in entity.__dict__])
    print(colname)
    # 创建表中values的值
    colplaceholders = ','.join(["%%(%s)s" % col for col in entity.__dict__])
    print(colplaceholders)

    sql = sql % (table, colname, colplaceholders)
    print(sql)


if __name__ == '__main__':
    u1 = User()
    u1.money = 100000
    u1.phone = 15574673339
    u1.name = '公孙离'
    u1.id = 432930197987707890
    save(u1)

    o1 = Order()
    o1.price = 1000
    o1.title = '苹果最香'
    o1.number = 'macbookair'
    save(o1)
