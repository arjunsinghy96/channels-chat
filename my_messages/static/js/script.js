$('document').ready(function(){
    $('.dropdown-button').dropdown();
    var chatbox = document.getElementById('outer-chat-container');
    chatbox.scrollTop = chatbox.scrollHeight;
});
