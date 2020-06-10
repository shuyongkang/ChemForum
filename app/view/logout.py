from flask import Blueprint, session, redirect, url_for
from app.util import require_login

bp = Blueprint("logout", __name__)


# 清除缓存的用户信息，模板重新按照无email信息的要求加载
@bp.route('/logout', methods=['GET'])
@require_login
def logout():
    session.clear()
    return redirect(url_for('index.index'))
