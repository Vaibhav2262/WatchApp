document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.banner-images img');
    let currentIndex = 0;

    function showNextImage() {
        images[currentIndex].classList.remove('visible');
        currentIndex = (currentIndex + 1) % images.length;
        images[currentIndex].classList.add('visible');
    }

    setInterval(showNextImage, 3000);
});
