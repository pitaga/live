/*
    视频、音频、分享屏幕选择
 */
window.onload = function() {
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.commander = channel.objects.commander;  // 此处channel.objects.printer中的printer就是上文提到的功能类注册的标识名
    });
};
function sendCommand() {
    commander.executeCommand($('#select_command').val());
}


/*
    以下为视频拉流js源码（从rtmp上拉流）
*/
//设置本地flash插件地址
videojs.options.flash.swf = "./static/js/video-js.swf";
// 初始化视频，设为全局变量
var myPlayer = videojs('myLive', {
    autoplay: true,
    controls: true,//控制条
    techOrder: ["flash"],//设置flash播放
    muted: true,// 静音
    preload: "auto",// 预加载
    language: "zh-CN",// 初始化语言
    playbackRates: [1, 2, 3, 4, 5, 8, 10, 20]// 播放速度
}, function () {
    console.log("--------------成功初始化视频--------------");
    myPlayer.one("playing", function () {         // 监听播放
        console.log("开始播放");
    });
    myPlayer.one("error", function (error) {      // 监听错误
        console.error("监听到异常，错误信息：%o",error);
    });
});



/*
    以下为聊天js源码
 */
// 全局变量username
var username = "";
$.post("/audience", {message:""}, function(data){
    username = data;
    console.log("用户名：" + username);
});
var ws = new WebSocket("ws://192.168.31.166:9999/chat");
// 向服务器发送消息
function sendMessage() {
    var message = JSON.stringify({
        "type": "message",
        "username": username,
        "message": $('#chat_content').val()
    });
    ws.send(message);
    $('#chat_content').val("");
}
// 从服务器接收消息
ws.onmessage = function (mess) {
    var obj = JSON.parse(mess.data);
    console.log("username:" + obj.username + "\tmessage:" + obj.message);
    if (username === obj.username) {
        $('#chat_log').append("<div class='chat_message_self'>" + obj.message +
            ":<b'>" + obj.username + "</b></div>");
    }
    else {
        $('#chat_log').append("<div class='chat_message'><b>" + obj.username +
            "</b>:" + obj.message + "</div>");
    }
};