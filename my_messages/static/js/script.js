$('document').ready(function(){
    $('.modal').modal();
    $('.dropdown-button').dropdown();
    var chatbox = document.getElementById('chat-container');
    chatbox.scrollTop = chatbox.scrollHeight;
});
