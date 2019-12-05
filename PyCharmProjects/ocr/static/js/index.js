// 建立WebSocket连接
var ws = new WebSocket("ws://10.40.33.167:8000/home");


// 获取canvas对象
var c = document.getElementById("canvas_image");
var ctx = c.getContext("2d");

// 轨迹实时预览
if (document.body.ontouchstart===undefined) {
    // mouse事件,web端鼠标
    c.width = window.screen.width * 0.3;
    c.height = window.screen.height * 0.28;
    c.onmousedown = function (e) {
        var ox = e.clientX - c.offsetLeft;
        var oy = e.clientY - c.offsetTop;
        ctx.moveTo(ox, oy);
        document.onmousemove = function (e) {
            var ox2 = e.clientX - c.offsetLeft;
            var oy2 = e.clientY - c.offsetTop;
            ctx.lineTo(ox2, oy2);
            ctx.stroke();
        };
        document.onmouseup = function (e) {
            document.onmousemove = null;
            document.onmouseup = null;
        }
    }
}
else {
    // 定义触屏事件
    c.width = window.screen.width * 1.45;
    c.height = window.screen.height * 0.5;
    // 触屏事件
    var start_x, start_y, move_x, move_y, end_x, end_y;

    var t = c.offsetTop;//canvas上边距
    var l = c.offsetLeft;//canvas做边距
    //按下
    c.addEventListener("touchstart",function(e){
        start_x = e.touches[0].pageX - l;
        start_y = e.touches[0].pageY - t;
        //显示坐标
        document.getElementById('position').innerText = (`${start_x}, ${start_y}`);
    });
    //移动
    c.addEventListener("touchmove",function(e){
        move_x = e.touches[0].pageX - l;
        move_y = e.touches[0].pageY - t;
        //显示坐标
        document.getElementById('position').innerText = (`${move_x}, ${move_y}`);
    });
    //松开
    c.addEventListener("touchend",function(e){
        end_x = e.changedTouches[0].pageX - l;
        end_y = e.changedTouches[0].pageY - t;
        //显示坐标
        document.getElementById('position').innerText = (`${end_x}, ${end_y}`);
    });
    // 开始绘画
    c.addEventListener("touchstart",function(e){
        start_x = e.touches[0].pageX - l;
        start_y = e.touches[0].pageY - t;
        //开始本次绘画
        ctx.beginPath();
        //画笔起始点
        ctx.moveTo(start_x, start_y);
        //显示坐标
        document.getElementById('position').innerText = (`${start_x}, ${start_y}`);
    });
    // 根据鼠标路径绘画
    c.addEventListener("touchmove",function(e){
        move_x = e.touches[0].pageX - l;
        move_y = e.touches[0].pageY - t;
        //根据鼠标路径绘画
        ctx.lineTo(move_x, move_y);
        //立即渲染
        ctx.stroke();
        //显示坐标
        document.getElementById('position').innerText = (`${move_x}, ${move_y}`);
    });
    // 创建从当前点到开始点的路径
    c.addEventListener("touchend",function(e){
        end_x = e.changedTouches[0].pageX - l;
        end_y = e.changedTouches[0].pageY - t;
        //创建从当前点到开始点的路径
        ctx.closePath();
        //显示坐标
        document.getElementById('position').innerText = (`${end_x}, ${end_y}`);
    });
}


// 发送图片到后端
function sendImage() {
    ws.send(c.toDataURL("image/png"));
}


// 清空画布
function clearCanvas() {
    window.location.reload();
}


// 显示结果
ws.onmessage = function (mess)
{
    var result = document.createElement("p");
    result.append(mess.data);
    result.className = "result_label";
    document.getElementById("result_content").append(result);
};
