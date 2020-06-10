import os
from flask import Flask, session
from app.models import query_user_info
from app.view import index, login, logout, person, register, \
    post_issue, view_issue, list_issue

app = Flask(__name__)
app.secret_key = os.urandom(128)

app.register_blueprint(index.bp)
app.register_blueprint(login.bp)
app.register_blueprint(logout.bp)
app.register_blueprint(person.bp)
app.register_blueprint(register.bp)
app.register_blueprint(post_issue.bp)
app.register_blueprint(view_issue.bp)
app.register_blueprint(list_issue.bp)


# 获得登录状态/用户信息
# 将email作为一个变量在所有模板中可见
# 模板根据email变量决定是否渲染用户信息
@app.context_processor
def check_user_cookie():
    email = session.get('email')
    if email:
        try:
            user = query_user_info(email)
            if user:
                return {
                    'email': user['email'],
                    'username': user['username'],
                    'user_type': user['level']
                }
        except Exception as e:
            raise e
    return {}
