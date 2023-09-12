
// app.js
$(document).ready(function () {
    // Event listener for the "Like" button click
    $(".like-button").click(function () {
        const warbleId = $(this).data("warble-id");

        // Send an AJAX request to the server to like/unlike the warble
        $.ajax({
            url: `/like-warble/${warbleId}`, // Replace with your Flask route
            method: "POST",
            success: function (data) {
                // Update the button or UI based on the response
                if (data.success) {
                    // The warble was liked/unliked successfully
                    // Update the UI accordingly
                    if (data.isLiked) {
                        $(this).find("i").removeClass("bi-star").addClass("bi-star-fill");
                    } else {
                        $(this).find("i").removeClass("bi-star-fill").addClass("bi-star");
                    }
                }
            },
            error: function (error) {
                console.error("Error:", error);
            },
        });
    });
});
