//建立websocket连接
var ws = new WebSocket("ws://10.40.32.236:8000/home");

//读取本地文件
var inputOne = document.getElementById('picture');
inputOne.onchange = function () {
    var fileList = inputOne.files;  //获取选中的文件列表
    var file = fileList[0];
    var reader = new FileReader();  //读取文件内容
    reader.readAsDataURL(file);
    reader.onload = function (e) {
        showCanvas(reader.result);  //将结果显示到canvas
    }
};
//指定图片内容显示
function showCanvas(dataUrl) {
    console.info(dataUrl);
    var canvas = document.getElementById('myCanvas');
    var ctx = canvas.getContext('2d');
    //加载图片
    var img = new Image();
    img.onload = function () {
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    };
    img.src = dataUrl;
}
//缩放canvas图片
function resizeImage(ImgD, FitWidth, FitHeight) {
    var image = new Image();
    image.src = ImgD.src;
    if (image.width > 0 && image.height > 0) {
        if (image.width / image.height >= FitWidth / FitHeight) {
            if (image.width > FitWidth) {
                ImgD.width = FitWidth;
                ImgD.height = (image.height * FitWidth) / image.width;
            } else {
                ImgD.width = image.width;
                ImgD.height = image.height;
            }
        } else {
            if (image.height > FitHeight) {
                ImgD.height = FitHeight;
                ImgD.width = (image.width * FitHeight) / image.height;
            } else {
                ImgD.width = image.width;
                ImgD.height = image.height;
            }
        }
    }
    return image;
}


//点击按钮，发送图片到服务器
function sendMessage() {
    var canvas = document.getElementById('myCanvas');
    ws.send(canvas.toDataURL("image/png"));
}


//在网页上显示结果
ws.onmessage = function (mess)
{
    var base = "the flower is ";
    var result = base + mess.data;
    self.alert(result);
};
