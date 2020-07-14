import pymysql
import base64
'''

create table content(
    create_date timestamp DEFAULT CURRENT_TIMESTAMP,
    content longblob NOT NULL
)charset=utf8;

'''
'''
create database yyx_reminder
'''


class my_database:
    def __init__(self, host, port, user, password, db, charset='utf8'):
        self.mysql = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset=charset,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.cursor = self.mysql.cursor()

    def create_table(self):
        self.cursor.execute('create table content(\
            create_date timestamp  DEFAULT CURRENT_TIMESTAMP,\
            content longblob NOT NULL\
            )charset=utf8;')

    def get_content_by_date(self, _date):
        cmd = 'select * from content where date_format(create_date, \'%Y-%m-%d\')=\''+_date+'\''
        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    def insert(self, content):
        cmd = 'insert into content (content) values (\'' + content + '\')'
        print(cmd)
        self.cursor.execute(cmd)

    def clear(self):
        cmd = 'drop table content'
        self.cursor.execute(cmd)
        self.create_table()

    def get_all_content(self):
        cmd = 'select * from content'
        self.cursor.execute(cmd)
        return self.cursor.fetchall()