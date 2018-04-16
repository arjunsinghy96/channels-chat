var username = $("#id_username").text();
var addr = 'ws://' + window.location.host + window.location.pathname;

var socket = new WebSocket(addr);

socket.onmessage = function(msg) {
    var data = JSON.parse(msg.data);
    console.log(data);
    if(username === data.handle){
        var message = `
            <div class="row mt-2 justify-content-end">
                <div class="col-8 mr-2 float-right bubble-me">
                    <div>${data.message}</div>
                    <small class="float-right">${data.sent_at}</small>
                </div>
            </div>`
    }
    else{
        var message = `
            <div class="row mt-2">
                <div class="col-8 ml-2 float-left bubble-other text-white">
                    <div><strong>${data.handle}</strong></div>
                    <div>${data.message}</div>
                    <small class="float-right">${data.sent_at}}</small>
                </div>
            </div>`
    }
    $('main').append(message);
};

if(socket.readyState == socket.OPEN) socket.onopen();

$('#id_form_msg_box').on('submit', function(e) {
    var msg=$('#id_msg_box').val();
    socket.send(msg);
    $('#id_msg_box').val('');
    return false;
});