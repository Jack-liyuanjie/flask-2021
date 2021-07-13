import hashlib

from dao import BaseDao


class UserDao(BaseDao):
    def list(self):

        return super().find_all('user')

    def login(self, name, password):
        # dao = BaseDao()
        # 如果密码时哈希码的话需要转码操作
        # psd = hashlib.md5('123456'.encode('utf-8').hex())
        result = super().find_all('user', ' where name=%s and password=%s', name, password)
        if result:
            return result[0]

    def save(self, **data):
        return super().save('user', **data)

    def update(self, **data):
        if not data.get('id'):
            return False

        id = data.pop('id')

        # 密码加密
        # if data.get('password'):
        #     data['password'] = hashlib.md5(data.get('password')).hexdigest()
        return super().update('user',id,**data)


if __name__ == '__main__':
    dao = UserDao()
    # 查找
    # user = dao.login('李元杰', '123456')
    # print(user)

    # 注册
    # user = dict(name='王大锤',
    #             password='123456',
    #             phone='1233768906')
    #
    # result = dao.save(**user)
    # print(result)

    # 更新
    update_user = dict(id=4,name="马大锤")

    print(dao.update(**update_user))
