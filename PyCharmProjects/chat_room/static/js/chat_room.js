// 进入界面直接调用ajxa请求
var mess = "正在跳转";
$.post("/home", {message:mess}, function(data){
    username = data;
});
// 建立websocket链接
var ws = new WebSocket("ws://10.70.22.109:8000/chat");
chat_room = "default";      // 当前所在聊天室
last_chat_room = "";        // 上一个聊天室
room_name = "";             // 用户输入的聊天室名称临时变量



// 默认聊天室事件
function enter_default() {
    last_chat_room = chat_room;
    chat_room = "默认聊天室";
    $('#chat_log_label').innerHTML = chat_room;
    if (chat_room != last_chat_room) {
        $('#chat_log').html("");
        var initialize_message = JSON.stringify({
            "type": "enter_room",
            "username": username,
            "chat_room": chat_room,
            "last_room": last_chat_room,
        });
        ws.send(initialize_message);
    }
}
// 创建聊天室按钮
function create_room() {
    room_name = self.prompt("输入聊天室名称");
    if (room_name != null) {
        var new_room = '<button class="room_default" onclick="enter_self()">' + room_name + '</button>';
        var create_message = JSON.stringify({
            "type": "button",
            "button": new_room,
            "chat_room": room_name,
            "username": username,
        });
        ws.send(create_message);
        self.alert(room_name + " 聊天室创建成功，点击 " + room_name + " 即可进入聊天室");
    } else {
        self.alert("创建失败");
    }
}
// 进入当前按钮所代表的聊天室
function enter_self() {
    last_chat_room = chat_room;
    chat_room = room_name;
    $('#chat_log_label').innerHTML = chat_room;
    if (chat_room != last_chat_room) {
        $('#chat_log').html("");
        var initialize_message = JSON.stringify({
            "type": "enter_room",
            "username": username,
            "chat_room": chat_room,
            "last_room": last_chat_room,
        });
        ws.send(initialize_message);
    }
}



// 向服务器发送消息
function sendMessage() {
    var message = JSON.stringify({
        "type": "message",
        "username": username,
        "message": $('#chat_content').val(),
        "chat_room": chat_room,
    });
    ws.send(message);
    $('#chat_content').val("");
}
// 从服务器接收消息
ws.onmessage = function (mess) {
    // $('#chat_log').append("<p>" + mess.data + "</p>")
    json_obj = JSON.parse(mess.data);
    var type = json_obj.type;
    if (type == "message") {
        var content = json_obj.content;
        $('#chat_log').append("<p>" + content + "</p>");
    } else if (type == "button") {
        room_name = json_obj.room_name;
        var button = json_obj.button;
        $('#chat_room').append(button);
    } else if (type == "enter_room") {
        var content = json_obj.content;
        $('#chat_log').append("<p>" + content + "</p>");
    } else if (type == "chat_log") {
        var log_obj = json_obj.chat_log;
        var history = json_obj.history;
        for (let index in log_obj) {
            $('#chat_log').append("<p>" + log_obj[index] + "</p>");
        }
        $('#chat_log').append("<p>" + history + "</p>");
    }
};
