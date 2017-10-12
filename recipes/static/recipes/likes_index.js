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
        $('.like').click(function(){
                var csrftoken = getCookie('csrftoken');
                var id = '#' + $(this).attr('id');
                var rid = $(id).attr("data-rid");
                var count = $('#' + rid).text();
                count = parseInt(count);
                $.post('/recipes/like/' + rid + '/', {'csrfmiddlewaretoken': csrftoken});
                count++;
                $('#' + rid).html(count);
                $('#unlike_' + rid).show();
                $('#like_' + rid).hide();
                });
        
        $('.unlike').click(function(){
                var csrftoken = getCookie('csrftoken');
                var id = '#' + $(this).attr('id');
                var rid = $(id).attr("data-rid");
                var count = $('#' + rid).text();
                count = parseInt(count);
                $.post('/recipes/unlike/' + rid + '/', {'csrfmiddlewaretoken': csrftoken});
                count--;
                $('#' + rid).html(count);
                $('#unlike_' + rid).hide();
                $('#like_' + rid).show();
        });
        $('.add_cookbook').click(function(){
                var csrftoken = getCookie('csrftoken');
                var id = '#' + $(this).attr('id');
                var rid = $(id).attr("data-rid");
                $.post('/recipes/add_to_cookbook/' + rid + '/', {'csrfmiddlewaretoken': csrftoken});
                $('#add_cookbook_' + rid).hide();
                $('#remove_cookbook_' + rid).show();
        });
        $('.remove_cookbook').click(function(){
                var csrftoken = getCookie('csrftoken');
                var id = '#' + $(this).attr('id');
                var rid = $(id).attr("data-rid");
                $.post('/recipes/remove_from_cookbook/' + rid + '/', {'csrfmiddlewaretoken': csrftoken});
                $('#add_cookbook_' + rid).show();
                $('#remove_cookbook_' + rid).hide();
        });
});
