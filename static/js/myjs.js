$(document).ready(function() {
    $('.like-button').on('click', function(e) {
        e.preventDefault();
        var recipeId = $(this).data('recipe-id');
        var likeCount = $(this).siblings('.like-count');
        
        $.ajax({
            url: 'cook/like_recipe/' + recipeId + '/',
            method: 'GET',
            success: function(data) {
                likeCount.text(data.likes);
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});