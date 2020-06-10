// 随机生成文件名
function getRandomFileName(len = 128) {
    let chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
    let filename = "";
    let now = (new Date()).toJSON();
    for (let i = 0; i < len - now.length; i++) {
        filename += chars[Math.floor(Math.random() * chars.length)];
    }
    return filename + now;
}

// 选择本地文件作为新头像以后的动作
document.querySelector('#btn_file').onchange = function () {
    if (this.files.length) {
        let file = this.files[0];
        let reader = new FileReader();
        reader.onload = function () {
            let img = new Image();
            img.src = this.result;
            img.onload = function () {
                let canvas = document.getElementById('canvasInput');
                canvas.width = 120;
                canvas.height = 120;
                [canvas.offsetWidth, canvas.offsetHeight] = [canvas.width, canvas.height];
                const ctx = canvas.getContext('2d');
                ctx.drawImage(this, 0, 0, canvas.width, canvas.height);
                let filename = getRandomFileName(32);
                let savename = '/static/img/' + filename + '.png';
                let data = {
                    'imageBase64': canvas.toDataURL("image/png", 1.0),
                    'saveName': savename
                };
                $.post('/person/upload_img', data, function () {
                    document.getElementById("pho").src = savename;
                    data = {
                        'signature': document.getElementById("sig").innerText,
                        'profile_photo': savename,
                        "username": document.getElementById("un").innerText
                    };
                    $.post('/person/change_info/pho', data, function () {
                    });
                });
            }
        };
        reader.readAsDataURL(file);
    }
}

// 点击头像，拉起隐藏的文件选择框
function change_profile_photo() {
    document.getElementById("btn_file").click();
}

//修改用户名时发送post请求
function change_username() {
    let old_text = document.getElementById("un").innerText;
    let new_text = prompt('新用户名：', old_text);
    if (new_text == "" || old_text == new_text) return;
    let data = {
        'signature': null,
        'profile_photo': null,
        "username": new_text
    };
    $.post('/person/change_info/un', data, function () {
        document.getElementById("un").innerText = new_text;
    });
}

//修改签名时发送post请求
function change_signature() {
    let old_text = document.getElementById("sig").innerText;
    let new_text = prompt('新签名：', old_text);
    if (new_text == "" || old_text == new_text) return;
    let data = {
        'signature': new_text,
        'profile_photo': null,
        "username": null
    };
    $.post('/person/change_info/sig', data, function () {
        document.getElementById("sig").innerText = new_text;
    });
}
