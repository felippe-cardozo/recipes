$(document).ready(function(){        
        $('#like').click(function(){
                var rid;
                rid = $(this).attr("data-rid");
                $.get('/recipes/like/', {recipe_id: rid}, function(data){
                $('#likes_count').html(data);
                $('#unlike').show();
                $('#like').hide();
                });
        });
        $('#unlike').click(function(){
                var rid;
                rid = $(this).attr("data-rid");
                $.get('/recipes/unlike/', {recipe_id: rid}, function(data){
                        $('#likes_count').html(data);
                        $('#unlike').hide();
                        $('#like').show();
                });
        });
});
