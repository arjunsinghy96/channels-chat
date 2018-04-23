var username = $("#id_username").text();
var addr = 'ws://' + window.location.host + window.location.pathname;

var socket = new WebSocket(addr);

socket.onmessage = function(msg) {
    var data = JSON.parse(msg.data);
    if(data.type == "message:new"){
        var message = data.content.message
        if(message.type == "text"){
            if(username === message.sender){
                var message = `
                    <div class="row mt-2 justify-content-end">
                        <div class="col-8 mr-2 float-right bubble-me">
                            <div>${message.text}</div>
                            <small class="float-right">${message.sent_at}</small>
                        </div>
                    </div>`
            }
            else{
                var message = `
                    <div class="row mt-2">
                        <div class="col-8 ml-2 float-left bubble-other text-white">
                            <div><strong>${message.sender}</strong></div>
                            <div>${message.text}</div>
                            <small class="float-right">${message.sent_at}}</small>
                        </div>
                    </div>`
            }
            $('main').append(message);
        }
    }
    
    
};

if(socket.readyState == socket.OPEN) socket.onopen();

$('#id_form_msg_box').on('submit', function(e) {
    var msg=$('#id_msg_box').val();
    var urgent = $('#id-urgent');
    data = {
        msg: msg,
        urgent: Boolean(urgent.attr('checked')),
    }
    socket.send(JSON.stringify(data));
    $('#id_msg_box').val('');
    urgent.attr('checked', false)
    $('#id-bolt').removeClass('text-warning');
    return false;
});

$('#id-bolt').click(function(){
    $(this).toggleClass('text-warning');
    var urgent = $('#id-urgent')
    urgent.attr('checked', !urgent.attr('checked'));
})