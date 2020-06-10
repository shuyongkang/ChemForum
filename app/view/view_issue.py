import datetime, time
from flask import Blueprint, request, render_template, session, redirect, url_for
from app.models import query_issue_info, query_answer_info, post_answer_info
from app.util import get_rand_id, require_login

bp = Blueprint("view_issue", __name__)


# 单个问题查看的后端实现
@bp.route('/view_issue/<ino>', methods=['GET', 'POST'])
@require_login
def view_issue(ino):
    # 查看问题时刷新界面
    if request.method == 'GET':
        try:
            if request.method == 'GET':
                issue = query_issue_info(ino)
                answer = query_answer_info(ino)
                return render_template(
                    'view_issue.html',
                    ino=ino,
                    issue_title=issue['title'],
                    answer=answer,
                    issue_content=issue['content']
                )
        except Exception as e:
            raise e
    # 提交回答时刷新界面
    if request.method == 'POST':
        ino = request.values.get('ino')
        email = session.get('email')
        answer = request.values.get('editorValue')
        create_time = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            # 随机数+时间戳作为128位id，不进行查重检测
            s = str(datetime.datetime.now().utcnow())
            ano = get_rand_id(128 - len(s)) + s
            post_answer_info(ano, ino, answer, create_time, email)
            # 下面会执行get请求刷新页面
            return redirect(url_for('view_issue.view_issue', ino=ino))
        except Exception as e:
            raise e
