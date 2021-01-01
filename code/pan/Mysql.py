import pymysql

# 1，连接数据库
# 2， 创建uer表
# 3， 读取uer表
# 4， 创建custom_account表
# 5， 插入custom_account表
# 6， 查询custom_account表
# 7， 创建custom_indextree表
# 8， 插入custom_indextree表
# 9， 查询custom_indextree表

class MySQL(object):
    def __init__(self):
        self.mydb = None
        self.cursor = None

        self.user = ["receiver", "manager", "connect", "access_control", "audit"]
        self.grade = [0, 0, 1, 0, 2]

    def connect_mysql(self, host, user, passwd, db):
        try:
            self.mydb = pymysql.connect(host, user, passwd, db)
            self.cursor = self.mydb.cursor()
        except:
            print("MySQL: can not connect mysql!")

    def create_user_table(self):
        select_sql = "show tables;"
        create_sql = "create table user(uid char(20), grade int);"
        begin_sql = "begin;"
        commit_sql = "commit;"
        try:
            self.cursor.execute(select_sql)
            results = self.cursor.fetchall() #results type: tuple
            exit_user = 0
            for table in results:
                if table == "user":
                    exit_user = 1
            if exit_user == 0:
                try:

                    self.cursor.execute(create_sql)    #建表时就已经提交，无法删除事务
                    self.cursor.execute(begin_sql)     #开始事务
                    for pos in range(len(self.user)):
                        insert_sql = "insert into user (uid, grade) values ('%s', %d);" % (self.user[pos], self.grade[pos])
                        self.cursor.execute(insert_sql)
                    self.cursor.execute(commit_sql)
                except:
                    print("MySQL: rollback")
                    self.mydb.rollback()
        except:
            print("MySQL: can not show tables")

    def select_user(self):
        select_sql = "select * from user;"
        try:
            self.cursor.execute(select_sql)
            results = self.cursor.fetchall()
            print(results)
        except:
            print("MySQL: can not select user")

    def create_custom_account(self):
        pass

    def insert_custom_account(self, custom_id, account, passwd):
        pass

    def select_custom_account(self, custom_id):
        pass

    def create_coustom_indextree(self):
        pass

    def insert_coustom_indextree(self, custom_id, indextree):
        pass

    def select_coustom_indextree(self):
        pass

m = MySQL()
m.connect_mysql("localhost", "root", "sk199813", "mypan")
m.create_user_table()
m.select_user()