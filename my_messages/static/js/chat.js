var username = $("#id_username").text();
var addr = 'ws://' + window.location.host + window.location.pathname;

console.log(addr)
var socket = new WebSocket(addr);

socket.onmessage = function(msg) {
    var data = JSON.parse(msg.data);
    console.log(data);
    if(username === data.handle){
        var classes= "col s8 push-s4 z-depth-1 message-bubble me grey lighten-2";
    }
    else{
        var classes = "col s8 pull-s0 z-depth-1 message-bubble other cyan darken-4 white-text";
    }
    var message = `<div class="${classes}">
                     <p><b>${data.handle}</b></p>
                     <p>${data.message}</p>
                   </div>`

    $('#id_chat').prepend(message);
};

if(socket.readyState == socket.OPEN) socket.onopen();

$('#id_form_msg_box').on('submit', function(e) {
    var msg=$('#id_msg_box').val();
    socket.send(msg);
    $('#id_msg_box').val('');
    return false;
});
