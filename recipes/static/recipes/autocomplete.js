$(document).ready(function(){
        $('#search').autocomplete({
                source: "/recipes/suggestions",
        });
});
