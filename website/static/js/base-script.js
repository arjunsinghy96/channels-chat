window.searchTimeout = 0

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
            $('#invite-count').attr('data-count', data.count)
        }
    })
})

var search_league = function(key){
    var results = $.ajax({
        method: 'GET',
        url: '/search/league/?q=' + $('#league-search-box').val(),
        success: function(results){
            if(results.length > 0){
                var dd = $('#league-search-dropdown');
                dd.html('');
                results.forEach(function(name){
                    dd.append('<a class="dropdown-item text-center clickable-results">' + name + '</a>')
                })
            }
            else{
                $('#league-search-dropdown').html('')
                $('#league-search-dropdown').append('<a class="dropdown-item text-center" href="#">' + 'No results' + '</a>')
            }
        }
    })
}

$('#name-edit').click(function(){
    $('#name').toggleClass('d-none');
    $('#name-form').toggleClass('d-none');
})

$('#name-form-close').click(function(){
    $('#name').toggleClass('d-none');
    $('#name-form').toggleClass('d-none');
})

$('#phone-edit').click(function(){
    $('#phone').toggleClass('d-none');
    $('#phone-form').toggleClass('d-none');
})

$('#phone-form-close').click(function(){
    $('#phone').toggleClass('d-none');
    $('#phone-form').toggleClass('d-none');
})

$('#show-search').click(function(){
    $('#search-box').toggleClass('d-none');
})

$('#close-search').click(function(){
    $('#search-box').toggleClass('d-none');
})

$('input[name=league-name]').keyup(function(){
    clearTimeout(searchTimeout)
    window.searchTimeout = setTimeout(
        search_league,
        500,
        $(this).val()
    )
})