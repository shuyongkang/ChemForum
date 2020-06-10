import random, string
from functools import wraps
from flask import session, redirect, url_for


# 返回长度为 id_length 的随机字符串
def get_rand_id(id_length=128):
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(id_length)]
    random_str = ''.join(str_list)
    return random_str


# 利用装饰器限制部分页面的访问，如果缺少登录信息，那么重定向到登录页面
def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('email'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login.login'))

    return wrapper
