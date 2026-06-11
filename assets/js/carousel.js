// carousel.js - Image carousel functionality for project pages

document.addEventListener('DOMContentLoaded', () => {
    // Initialize project carousel
    const carousel = document.querySelector('.project-carousel');
    if (!carousel) return;
    
    const carouselInner = carousel.querySelector('.carousel-inner');
    const items = carousel.querySelectorAll('.carousel-item');
    const prevBtn = carousel.querySelector('.carousel-prev');
    const nextBtn = carousel.querySelector('.carousel-next');
    
    if (!carouselInner || !items.length || !prevBtn || !nextBtn) return;
    
    let currentIndex = 0;
    const totalItems = items.length;
    
    // Update carousel position
    function updateCarousel() {
        carouselInner.style.transform = `translateX(-${currentIndex * 100}%)`;
        
        // Update active state for items
        items.forEach((item, index) => {
            if (index === currentIndex) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }
    
    // Previous button click handler
    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel();
    });
    
    // Next button click handler
    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel();
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', event => {
        if (event.key === "ArrowLeft") {
            currentIndex = (currentIndex - 1 + totalItems) % totalItems;
            updateCarousel();
        } else if (event.key === "ArrowRight") {
            currentIndex = (currentIndex + 1) % totalItems;
            updateCarousel();
        }
    });
    
    // Touch support for mobile
    let touchStartX = 0;
    let touchEndX = 0;
    
    carousel.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    carousel.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });
    
    function handleSwipe() {
        const swipeThreshold = 50; // Minimum distance to register as swipe
        
        if (touchEndX < touchStartX - swipeThreshold) {
            // Swipe left - go to next
            currentIndex = (currentIndex + 1) % totalItems;
            updateCarousel();
        } else if (touchEndX > touchStartX + swipeThreshold) {
            // Swipe right - go to previous
            currentIndex = (currentIndex - 1 + totalItems) % totalItems;
            updateCarousel();
        }
    }
    
    // Initialize carousel
    updateCarousel();
});
