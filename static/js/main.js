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
        backToTop = document.getElementById('#backToTop');

        if (window.scrollY > 300) {
            backToTop.style.display = 'block';
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


// Wishlist functionality
document.addEventListener('DOMContentLoaded', function() {
    const wishlistCounter = document.querySelector('.wishlist-counter');
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];

    function updateWishlistCounter() {
        wishlistCounter.textContent = wishlist.length;
    }

    function toggleWishlist(productId) {
        const index = wishlist.indexOf(productId);
        if (index > -1) {
            wishlist.splice(index, 1);
        } else {
            wishlist.push(productId);
        }
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
        updateWishlistCounter();
    }

    document.querySelectorAll('.wishlist-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = parseInt(this.dataset.productId, 10);
            toggleWishlist(productId);
            this.querySelector('.wishlist-icon').classList.toggle('text-danger');
            this.querySelector('.wishlist-icon').classList.toggle('text-muted');
        });
    });

    updateWishlistCounter();
});

document.addEventListener('DOMContentLoaded', function () {
    const wishlistCounter = document.querySelector('.wishlist-counter');
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];

    function updateWishlistCounter() {
        wishlistCounter.textContent = wishlist.length;
    }

    function toggleWishlist(productId, button) {
        const index = wishlist.indexOf(productId);
        if (index > -1) {
            wishlist.splice(index, 1);
        } else {
            wishlist.push(productId);
        }
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
        updateWishlistCounter();
        updateWishlistButtons();
    }

    function updateWishlistButtons() {
        document.querySelectorAll('.wishlist-btn').forEach(button => {
            const productId = parseInt(button.dataset.productId, 10);
            if (wishlist.includes(productId)) {
                button.querySelector('.wishlist-icon').classList.add('text-danger');
                button.querySelector('.wishlist-icon').classList.remove('text-muted');
            } else {
                button.querySelector('.wishlist-icon').classList.remove('text-danger');
                button.querySelector('.wishlist-icon').classList.add('text-muted');
            }
        });
    }

    document.body.addEventListener('click', function (event) {
        if (event.target.closest('.wishlist-btn')) {
            const button = event.target.closest('.wishlist-btn');
            const productId = parseInt(button.dataset.productId, 10);
            toggleWishlist(productId, button);
        }
    });

    updateWishlistCounter();
    updateWishlistButtons();
});

//  reload the page with the new category
document.getElementById('id_category').addEventListener('change', function() {
    
    this.form.submit();
});