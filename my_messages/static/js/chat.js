var username = $("#id_username").text();
var addr = 'ws://' + window.location.host + window.location.pathname;

console.log(addr)
var socket = new WebSocket(addr);

socket.onmessage = function(msg) {
    var data = JSON.parse(msg.data);
    console.log(data);
    if(username === data.handle){
        var outer_class = "row justify-content-end";
        var inner_class= "col-10 col-md-8 me message-bubble bg-green";
    }
    else{
        var outer_class = "row justify-content-start";
        var classes = "col-10 col-md-8 other message-bubble bg-blue";
    }
    var message = `<div class="${outer_class}">
                    <div class="${inner_class}">
                        <p><b>${data.handle}</b></p>
                        <p>${data.message}</p>
                   </div></div>`

    $('#chat-container').append(message);
    var chatbox = document.getElementById('outer-chat-container');
    chatbox.scrollTop = chatbox.scrollHeight;
};

if(socket.readyState == socket.OPEN) socket.onopen();

$('#id_form_msg_box').on('submit', function(e) {
    var msg=$('#id_msg_box').val();
    socket.send(msg);
    $('#id_msg_box').val('');
    return false;
});
