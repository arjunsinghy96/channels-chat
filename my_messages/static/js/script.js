var url = 'ws://' + window.location.host + window.location.pathname
console.log(url)

socket = new WebSocket(url)

socket.onmessage = function(e) {
    console.log(e.data)
        /*
    $('#id_chat_msgs').prepend('<p>' + e.data + '</p>');
    console.log(e);
    var data = json.parse(e.data);
    $('#id_chat').prepend('<tr>'
        + '<td>' + data['handle'] + '</td>'
        + '<td>' + data['message'] + '</td>'
        + '<td>' + data['timestamp'] + '</td>'
        + '</tr>'
        )
        */
}

socket.onopen = function() {
    socket.send('hello')
}

if (socket.readyState == socket.OPEN) socket.onopen();

$('#id_form_msg_box').on('submit', function(e) {
    var msg = $('#id_message_box').val();
    var handle = $('#id_handle').text();
    var room = window.location.pathname
    if(handle === undefined || handle === null || handle === '') {
        alert('Please provide a handle');
        return false;
    }
    var text = {'text': {'handle': handle, 'message': msg, 'room': room}}
    console.log(text);
    socket.send(JSON.stringify(text));
    return false;
});

$('#id_handle_form').on('submit', function(e) {
    console.log('handle handle handle');
    var handle = $('#id_handle_box').val();
    $('#id_handle').text(handle);
    return false;
});
