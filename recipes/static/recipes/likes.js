function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(document).ready(function(){        
        $('#like').click(function(){
                var csrftoken = getCookie('csrftoken');
                var rid = $(this).attr("data-rid");
                var count = parseInt($('#likes_count').text());
                $.post('/recipes/like/' + rid + '/', {'csrfmiddlewaretoken': csrftoken});
                count++;
                $('#likes_count').html(count);
                $('#unlike').show();
                $('#like').hide();
                });
        
        $('#unlike').click(function(){
                var csrftoken = getCookie('csrftoken')
                var rid = $(this).attr("data-rid");
                var count = parseInt($('#likes_count').text());
                $.post('/recipes/unlike/' + rid + '/', {'csrfmiddlewaretoken': csrftoken});
                count--;
                $('#likes_count').html(count);
                $('#unlike').hide();
                $('#like').show();
        });
});
