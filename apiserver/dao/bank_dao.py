from dao import BaseDao


class BankDao(BaseDao):
    def find_all(self):
        return super().find_all('bank')

if __name__ == '__main__':
    dao = BankDao()
    print(dao.find_all())