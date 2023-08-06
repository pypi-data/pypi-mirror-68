from db import MySQLTemplate


def func():
    result = MySQLTemplate.fetch_one('select * from user')
    print(result)
    _id = MySQLTemplate.insert('insert into user (`username`,`password`) values (%(username)s,%(password)s)',
                               {'username': '4', 'password': '4'})
    print(_id)


if __name__ == '__main__':
    func()
