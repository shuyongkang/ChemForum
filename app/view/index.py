import re, base64
from io import BytesIO
from PIL import Image
from flask import Blueprint, render_template, request, redirect, url_for
from app.util import require_login

bp = Blueprint("index", __name__)


@bp.route('/')
def index():
    return render_template('index.html')


# 约定，前端的json串用['imageBase64']和['saveName']字段发送数据
def save_img():
    data_url = request.values['imageBase64']
    filename = request.values['saveName']
    base64_data = re.sub('^data:image/.+;base64,', '', data_url)
    image_data = BytesIO(base64.b64decode(base64_data))
    img = Image.open(image_data)
    # app/views/../static/img/xxx.png = app/static/img/xxx.png
    filename = bp.root_path + '/..' + filename
    img.save(filename)


# 处理上传编辑器图片请求
@bp.route('/upload_img', methods=['POST'])
@require_login
def upload_img():
    if request.method == "POST":
        save_img()
        return redirect(url_for('post_issue.post_issue'))


# 处理上传用户头像请求
@bp.route('/person/upload_img', methods=['POST'])
@require_login
def upload_user_photo():
    if request.method == "POST":
        save_img()
        return redirect(url_for('person.person'))
