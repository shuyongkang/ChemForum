# 实现数据库查询操作
import time, pymysql

db = pymysql.connect(
    host='localhost',
    user='Admin4ChemForum',
    password='chemistry',
    db='ChemForumDataBase',
    port=3306
)


# 输入：要修改的用户信息，可修改的项包括签名、头像和用户名
def update_user_info(email, sig=None, pho=None, un=None):
    try:
        cursor = db.cursor()
        db.ping(reconnect=True)
        if sig is not None:
            sql = "update UserInfo set signature = '%s' where email = '%s'" % (sig, email)
            cursor.execute(sql)
        if pho is not None:
            sql = "update UserInfo set profile_photo = '%s' where email = '%s'" % (pho, email)
            cursor.execute(sql)
        if un is not None:
            sql = "update UserInfo set username = '%s' where email = '%s'" % (un, email)
            cursor.execute(sql)
        # 始终更新最近访问时间
        last_login_time = time.strftime("%Y-%m-%d %H:%M:%S")
        sql = "update UserInfo set last_login_time = '%s' where email = '%s'" % (last_login_time, email)
        cursor.execute(sql)
        db.commit()
        cursor.close()
    except Exception as e:
        raise e


# 输入：用户邮箱
# 输出：用户信息字典
# 查询失败返回空字典,修改最近登录时间
def query_user_info(email):
    try:
        cursor = db.cursor()
        sql = "select email,username,password,signature,create_time,profile_photo,last_login_time,level from UserInfo where email = '%s'" % email
        db.ping(reconnect=True)
        cursor.execute(sql)
        result = cursor.fetchone()
        # 始终更新最近访问时间
        last_login_time = time.strftime("%Y-%m-%d %H:%M:%S")
        sql = "update UserInfo set last_login_time = '%s' where email = '%s'" % (last_login_time, email)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        if result:
            return {
                'email': result[0],
                'username': result[1],
                'password': result[2],
                'signature': result[3],
                'create_time': result[4],
                'profile_photo': result[5],
                'last_login_time': result[6],
                'level': result[7],
            }
        else:
            return {}
    except Exception as e:
        raise e


# 输出：所有问题列表
def query_all_issues_info(email=None):
    try:
        cursor = db.cursor()
        if email is None:
            sql = "select ino,email,title,create_time,content from IssueInfo order by create_time desc"
        else:
            sql = "select ino,email,title,create_time,content from IssueInfo where email = '%s' order by create_time desc" % email
        db.ping(reconnect=True)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        raise e


# 输入：问题id
# 输出：问题回答列表
def query_answer_info(ino):
    try:
        cursor = db.cursor()
        sql = "select UserInfo.username,AnswerInfo.content,AnswerInfo.create_time,AnswerInfo.ano from AnswerInfo,UserInfo where AnswerInfo.email = UserInfo.email and ino = '%s' order by AnswerInfo.create_time desc" % ino
        db.ping(reconnect=True)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        raise e


# 输入：问题id
# 输出：问题信息字典
# 查询失败返回空字典
def query_issue_info(ino):
    try:
        cursor = db.cursor()
        sql = "select title,content from IssueInfo where ino = '%s'" % ino
        db.ping(reconnect=True)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        if result:
            return {
                'title': result[0],
                'content': result[1]
            }
        else:
            return {}
    except Exception as e:
        raise e


# 插入一条问题
def post_issue_info(ino, email, title, content, create_time):
    try:
        cursor = db.cursor()
        sql = "insert into IssueInfo(ino, email, title, content,create_time) VALUES ('%s','%s','%s','%s','%s')" \
              % (ino, email, title, content, create_time)
        db.ping(reconnect=True)
        cursor.execute(sql)
        db.commit()
        cursor.close()
    except Exception as e:
        raise e


# 插入一条用户信息
def post_user_info(email, username, password, level, create_time):
    try:
        cursor = db.cursor()
        sql = "insert into UserInfo(email, username, password, level, create_time) VALUES ('%s','%s','%s','%s','%s')" \
              % (email, username, password, level, create_time)
        db.ping(reconnect=True)
        cursor.execute(sql)
        db.commit()
        cursor.close()
    except Exception as e:
        raise e


# 插入一条回答
def post_answer_info(ano, ino, content, create_time, email):
    try:
        cursor = db.cursor()
        sql = "insert into AnswerInfo(ano, ino, content, create_time, email) VALUES ('%s','%s','%s','%s','%s')" \
              % (ano, ino, content, create_time, email)
        db.ping(reconnect=True)
        cursor.execute(sql)
        db.commit()
        cursor.close()
    except Exception as e:
        raise e
