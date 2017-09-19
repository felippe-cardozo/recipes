        $('#like').click(function(){
                var rid;
                rid = $(this).attr("data-rid");
                $.get('/recipes/like/', {recipe_id: rid}, function(data){
                $('#likes_count').html(data);
                $('#like').hide();
                });
        });
