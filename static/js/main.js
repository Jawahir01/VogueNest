// Navbar Scroll Effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Initialize Bootstrap components
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Toasts
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl);
    });

    // Initialize Dropdowns
    var dropdowns = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
    dropdowns.forEach(function(dropdownToggle) {
        new bootstrap.Dropdown(dropdownToggle);
    });

    // Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Back to Top Button
    const backToTop = document.createElement('div');
    backToTop.innerHTML = '<button class="btn btn-primary rounded-circle shadow" id="backToTop"><i class="fas fa-arrow-up"></i></button>';
    document.body.appendChild(backToTop);
    
    window.addEventListener('scroll', function() {
        backToTop = document.getElementById('backToTop');

        if (window.scrollY > 300) {
            document.getElementById('backToTop').style.display = 'block';
        } else {
            backToTop.style.display = 'none';
        }
    });

    document.getElementById('backToTop').addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});

// Product Image Zoom
document.querySelectorAll('.product-image').forEach(image => {
    image.addEventListener('click', function() {
        this.classList.toggle('zoomed');
    });
});

// Blog Read More Interactions
document.querySelectorAll('.btn-read-more').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();

        console.log('Reading more about:', this.closest('.blog-card').querySelector('.blog-title').textContent);
    });
});

// Enhanced Wishlist Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize wishlist
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    updateWishlistCounter();

    // Wishlist button handler
    document.querySelectorAll('.wishlist-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const icon = this.querySelector('.wishlist-icon');

            // Toggle wishlist state
            if (wishlist.includes(productId)) {
                wishlist = wishlist.filter(id => id !== productId);
                icon.classList.remove('text-danger');
                icon.classList.add('text-muted');
            } else {
                wishlist.push(productId);
                icon.classList.remove('text-muted');
                icon.classList.add('text-danger');
            }

            // Add animation
            icon.style.transform = 'scale(1.2)';
            setTimeout(() => icon.style.transform = '', 300);

            // Update storage and counter
            localStorage.setItem('wishlist', JSON.stringify(wishlist));
            updateWishlistCounter();
        });
        wishlist_counter = document.getElementById('wishlist-counter');
        wishlist_counter.addEventListener('click', function() {
            window.location.href = '/wishlist';
        });

    });

    // Update wishlist counter
    function updateWishlistCounter() {
        const counters = document.querySelectorAll('.wishlist-counter');
        counters.forEach(counter => {
            counter.textContent = wishlist.length;
        });
    }
}
);

document.addEventListener('DOMContentLoaded', function() {
        // Main image transition
        function changeMainImage(thumbnail) {
            const mainImage = document.getElementById('main-product-image');
            const newSrc = thumbnail.dataset.fullsize;
            
            // Add fade transition
            mainImage.style.opacity = '0';
            setTimeout(() => {
                mainImage.src = newSrc;
                mainImage.style.opacity = '1';
            }, 200);
        }
    
        // Initialize thumbnail click handlers
        document.querySelectorAll('.thumbnail-img').forEach(thumbnail => {
            thumbnail.addEventListener('click', function(e) {
                changeMainImage(this);
            });
        });
    
        // Quantity input controls
    function handleEnableDisable(input) {
        const currentValue = parseInt(input.value);
        const decrementBtn = input.parentNode.querySelector('.decrement-qty');
        const incrementBtn = input.parentNode.querySelector('.increment-qty');

        decrementBtn.disabled = currentValue < 2;
        incrementBtn.disabled = currentValue > 98;
    }

    // Initialize all quantity inputs
    document.querySelectorAll('.qty-input').forEach(input => {
        handleEnableDisable(input);
        
        input.addEventListener('change', () => {
            input.value = Math.max(1, Math.min(99, parseInt(input.value) || 1));
            handleEnableDisable(input);
        });
    });

    // Increment/decrement buttons
    document.querySelectorAll('.increment-qty, .decrement-qty').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const input = this.parentNode.querySelector('.qty-input');
            let currentVal = parseInt(input.value);

            if (this.classList.contains('increment-qty')) {
                input.value = currentVal < 99 ? currentVal + 1 : 99;
            } else {
                input.value = currentVal > 1 ? currentVal - 1 : 1;
            }

            handleEnableDisable(input);
        });
    });
    
        // Star rating hover effect
        document.querySelectorAll('.star-rating label').forEach(star => {
            star.addEventListener('mouseover', function() {
                const rating = this.htmlFor.replace('star', '');
                highlightStars(rating);
            });
    
            star.addEventListener('mouseleave', function() {
                const checked = document.querySelector('.star-rating input:checked');
                if (checked) {
                    highlightStars(checked.value);
                } else {
                    resetStars();
                }
            });
        });
    
        function highlightStars(rating) {
            document.querySelectorAll('.star-rating label').forEach((star, index) => {
                star.style.color = 5 - index <= rating ? '#ffc107' : '#ddd';
            });
        }
    
        function resetStars() {
            document.querySelectorAll('.star-rating label').forEach(star => {
                star.style.color = '#ddd';
            });
        }
}
);


//  reload the page with the new category
document.getElementById('id_category').addEventListener('change', function() {
    
    this.form.submit();
});