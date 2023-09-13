$('.like-button').on('click', function (e) {
    e.preventDefault();
    e.stopPropagation(); // Prevent the click event from propagating to the anchor link

    const button = $(this);
    const messageID = button.data('message-id');
    const isLiked = button.data('liked');

    // Send an AJAX request to like/unlike the message
    $.ajax({
        method: 'POST',
        url: `/users/add_like/${messageID}`,
        data: { liked: !isLiked },
        success: function (response) {
            // Update the button text and like status
            if (isLiked) {
                button.data('liked', false);
                button.html('<i class="far fa-heart"></i>');
            } else {
                button.data('liked', true);
                button.html('<i class="fas fa-heart"></i>');
            }
        }
    });
});


