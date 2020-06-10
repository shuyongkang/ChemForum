from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import query_user_info, update_user_info
from app.util import require_login

bp = Blueprint("person", __name__)


# 加载个人主页
@bp.route('/person', methods=['GET', 'POST'])
@require_login
def person():
    if request.method == 'GET':
        email = session.get('email')
        try:
            user_info = query_user_info(email)
        except Exception as e:
            raise e
        return render_template('person.html', user_info=user_info)


# 个人主页修改用户信息
@bp.route('/person/change_info/<target>', methods=['POST'])
@require_login
def change_info(target):
    if request.method == "POST":
        signature = request.values['signature']
        profile_photo = request.values['profile_photo']
        username = request.values['username']
        if target == 'sig':
            profile_photo = username = None
        elif target == 'pho':
            signature = username = None
        elif target == 'un':
            signature = profile_photo = None
        email = session.get('email')
        update_user_info(email, sig=signature, pho=profile_photo, un=username)
        try:
            user_info = query_user_info(email)
        except Exception as e:
            raise e
        return redirect(url_for('person.person', user_info=user_info))
