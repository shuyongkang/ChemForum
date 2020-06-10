from flask import Blueprint, request, render_template
from app.models import query_all_issues_info
from app.util import require_login

bp = Blueprint("list_issue", __name__)


@bp.route('/list_issue', methods=['GET', 'POST'])
@require_login
def list_issue():
    if request.method == 'GET':
        try:
            issue_detail = query_all_issues_info()
        except Exception as e:
            raise e
        return render_template('list_issue.html', issue_detail=issue_detail)
