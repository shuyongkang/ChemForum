//加载ueditor
let editor = UE.getEditor('main_editor', {
    initialContent: '输入内容...', autoClearinitialContent: true
});
let ready2ocr = true;//false:识别后，true:识别前
//加载画板
let canvas = document.getElementById('canvasInput');
[canvas.width, canvas.height] = [canvas.offsetWidth, canvas.offsetHeight];
let ctx = canvas.getContext('2d');
ctx.lineJoin = ctx.lineCap = 'round';
ctx.strokeStyle = 'black';
ctx.fillStyle = "white";
ctx.lineWidth = 2.5;
ctx.fillRect(0, 0, canvas.width, canvas.height);
let lastX, lastY, isDrawing = false, imgBuffer;
//完成鼠标画图逻辑
canvas.onmousedown = function (e) {
    ctx.lineWidth = 3;
    setReady(true);
    lastX = e.offsetX;
    lastY = e.offsetY;
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(lastX + 1, lastY + 1);
    ctx.stroke();
    isDrawing = true;
}
canvas.onmouseup = function (e) {
    isDrawing = false;
}
canvas.onmousemove = function (e) {
    if (isDrawing) {
        let x = e.offsetX;
        let y = e.offsetY;
        ctx.lineTo(x, y);
        ctx.stroke();
        lastX = x;
        lastY = y;
    }
}

//随机生成文件名
function getRandomFileName(len = 128) {
    let chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
    let filename = "";
    let now = (new Date()).toJSON();
    for (let i = 0; i < len - now.length; i++) {
        filename += chars[Math.floor(Math.random() * chars.length)];
    }
    return filename + now;
}

//向后台保存画布图片
//向在线编辑器插入img标签
function load2editor() {
    let filename = getRandomFileName(32);
    let savename = '/static/img/' + filename + '.png';
    let data = {
        'imageBase64': canvas.toDataURL("image/png", 1.0),
        'saveName': savename
    };
    $.post('/upload_img', data, function (data) {
        editor.execCommand('insertHtml', '&nbsp;<img src="' + savename + '" width=150px height=150px/>&nbsp;');
    });
    setReady();
}

//清空画布
function cls() {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    setReady();
    imgBuffer = new Image();
    imgBuffer.src = canvas.toDataURL("image/png", 1.0);
    imgBuffer.onload = function () {
        [canvas.width, canvas.height] = [canvas.offsetWidth, canvas.offsetHeight];
        ctx.drawImage(imgBuffer, 0, 0, canvas.width, canvas.height);
    }
}

//识别和回退功能
function recognize() {
    if (ready2ocr) {
        imgBuffer = new Image();
        imgBuffer.src = canvas.toDataURL("image/png", 0.8);
        imgBuffer.onload = function () {
            predict(canvas).then(
                result => handle(result)
            );

            function handle(result) {
                setReady(false);
                handleMolBoxes(canvas, result);
                let tmpImage = new Image();
                tmpImage.src = canvas.toDataURL("image/png", 1);
                tmpImage.onload = function () {
                    [canvas.width, canvas.height] = [canvas.offsetWidth, canvas.offsetHeight];
                    ctx.drawImage(tmpImage, 0, 0, canvas.width, canvas.height);
                }
            }
        }
    } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(imgBuffer, 0, 0, canvas.width, canvas.height);
        setReady();
    }
}

// 切换识别和回退功能
function setReady(toOCR = true) {
    if (toOCR) {
        document.getElementById('real_ocr_btn').innerText = '识别';
        ready2ocr = true;
    } else {
        document.getElementById('real_ocr_btn').innerText = '回退';
        ready2ocr = false;
    }
}

// 绑定图片上传按钮
document.querySelector('#img_file').onchange = function () {
    if (this.files.length) {
        let file = this.files[0];
        let reader = new FileReader();
        reader.onload = function () {
            let img = new Image();
            img.src = this.result;
            img.onload = function () {
                [canvas.width, canvas.height] = [canvas.offsetWidth, canvas.offsetHeight];
                ctx.fillStyle = "white";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                if (img.width > img.height)
                    ctx.drawImage(img, 0, 0, canvas.offsetWidth, img.height / img.width * canvas.offsetWidth)
                else
                    ctx.drawImage(img, 0, 0, img.width / img.height * canvas.offsetHeight, canvas.offsetHeight)
            }
        };
        setReady();
        reader.readAsDataURL(file);
    }
}
