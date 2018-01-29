var addr = 'ws://' + window.location.host + window.location.pathname;

console.log(addr)
var socket = new WebSocket(addr);

socket.onmessage = function(msg) {
    var data = JSON.parse(msg.data);
    console.log(data);
    $('#id_chat').prepend('<tr>'
            + '<td>' + data.handle + '</td>'
            + '<td>' + data.message + '</td>'
            + '<td>' + data.timestamp + '</td>'
            + '</tr>'
            )
};

if(socket.readyState == socket.OPEN) socket.onopen();

$('#id_form_msg_box').on('submit', function(e) {
    var msg=$('#id_msg_box').val();
    socket.send(msg);
    $('#id_msg_box').val('');
    return false;
});
