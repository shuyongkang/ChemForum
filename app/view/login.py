from flask import render_template, flash, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from flask import Blueprint
from app.models import query_user_info

bp = Blueprint("login", __name__)


# 处理登录请求
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not all([email, password]):
            flash("请完整填写登录信息！")
            return render_template('login.html')
        try:
            user_info = query_user_info(email);
            if user_info == {}:
                flash("用户不存在！")
                return render_template('login.html')
            if check_password_hash(user_info['password'], password):
                # 写浏览器缓存
                session['email'] = email
                session.permanent = True
                return redirect(url_for('index.index'))
            else:
                flash("密码错误！")
                return render_template('login.html')
        except Exception as e:
            raise e
