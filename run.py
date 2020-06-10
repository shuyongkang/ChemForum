from datetime import timedelta

from app import app

# 即时更新模板
app.jinja_env.auto_reload = True
# 即时更新缓存文件
app.send_file_max_age_default = timedelta(0)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
