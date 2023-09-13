const likeForms = document.querySelectorAll('.like-form');

likeForms.forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
        });

        // Handle the response and update the UI accordingly (toggle like button)
        if (response.ok) {
            const likeButton = form.querySelector('.like-button');
            const liked = likeButton.getAttribute('data-liked') === 'true';
            const isOwnWarble = likeButton.getAttribute('data-is-own-warble') === 'true';

            // Check if it's not the user's own warble before toggling
            if (!isOwnWarble) {
                toggleLikeButton(likeButton, liked);
            }

            // If it's the user's own warble, you can display a message here.
            if (isOwnWarble) {
                displayFlashMessage("You cannot like your own warbles", "danger");
            }
        }
    });
});

function toggleLikeButton(likeButton, liked) {
    likeButton.setAttribute('data-liked', liked ? 'false' : 'true');
    likeButton.innerHTML = liked ? '<i class="far fa-heart"></i>' : '<i class="fas fa-heart"></i>';
}

function displayFlashMessage(message, category) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${category}`;
    alert.textContent = message;

    const alertContainer = document.getElementById('alert-container');
    alertContainer.appendChild(alert);

    setTimeout(() => {
        alertContainer.removeChild(alert);
    }, 3000);
}
