import hashlib

from dao import BaseDao


class CardDao(BaseDao):
    def list(self):
        sql = """
            select c.id, c.number, c.money, u.name as username,b.name as bankname
            from card c 
            join user u on(u.id=c.user_id)
            join bank b on(b.id=c.bank_id)
        """
        result = super().query(sql)
        return result

    def save(self, **data):
        return super().save('user', **data)

    def update(self, **data):
        if not data.get('id'):
            return False

        id = data.pop('id')

        # 密码加密
        # if data.get('password'):
        #     data['password'] = hashlib.md5(data.get('password')).hexdigest()
        return super().update('user', id, **data)
