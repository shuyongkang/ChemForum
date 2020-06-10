import time
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models import query_issue_info, post_issue_info
from app.util import require_login, get_rand_id

bp = Blueprint("post_issue", __name__)

# 提问界面的后端
@bp.route('/post_issue', methods=['GET', 'POST'])
@require_login
def post_issue():
    if request.method == 'GET':
        return render_template('post_issue.html')
    # 提交问题后刷新界面
    if request.method == 'POST':
        title = request.form.get('title')
        email = session.get('email')
        if not title:
            flash("请输入问题标题！")
            return render_template('post_issue.html')
        content = request.form.get('editorValue')
        if content is None:
            content = ''
        create_time = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            ino = get_rand_id()
            issue_info = query_issue_info(ino)
            # 获得一个没用过的 issue id
            while issue_info != {}:
                ino = get_rand_id()
                issue_info = query_issue_info(ino)
            post_issue_info(ino, email, title, content, create_time)
            return redirect(url_for('view_issue.view_issue', ino=ino))
        except Exception as e:
            raise e
