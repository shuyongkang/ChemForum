import time
from flask import Blueprint, request, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from app.models import query_user_info, post_user_info

bp = Blueprint("register", __name__)


# 注册页面的后端
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password_1 = request.form.get('password_1')
        password_2 = request.form.get('password_2')
        if not all([email, username, password_1, password_2]):
            flash("请完整填写注册信息！")
            return redirect(url_for('register.register'))
        elif password_1 != password_2:
            flash("密码和确认密码不一致！")
            return redirect(url_for('register.register'))
        # 保存密码的哈希值
        password = generate_password_hash(password_1, method="pbkdf2:sha256", salt_length=8)
        try:
            result = query_user_info(email)
            if result != {}:
                flash("邮箱已注册！请登录或更换注册邮箱")
                return redirect(url_for('register.register'))
            else:
                create_time = time.strftime("%Y-%m-%d %H:%M:%S")
                post_user_info(email, username, password, '1', create_time)
                return redirect(url_for('login.login'))
        except Exception as e:
            raise e
