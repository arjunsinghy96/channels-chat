var username = $('#username').text()
var addr = 'ws://' + window.location.host + window.location.pathname + '?username=' + username;

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

$('form').on('submit', function(e) {
    var msg=$('#id_msg_box').val();
    socket.send(msg);
    return false;
});
