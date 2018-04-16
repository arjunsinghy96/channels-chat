$('document').ready(function(){
    $.ajax({
        method: 'GET',
        url: '/invites/count/',
        success: function(data){
            if(data.count === 0){
                return;
            }
            if(data.count > 99){
                $('#invite-count').html('99+');
            }
            else {
                $('#invite-count').html(data.count);
            }
        }
    })
})