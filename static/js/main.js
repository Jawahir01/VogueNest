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
    let toastElList = [].slice.call(document.querySelectorAll('.toast'));
    let toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl);
    });

    // Initialize Dropdowns
    let dropdowns = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
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

//  reload the page with the new category
document.getElementById('#id_category').addEventListener('change', function() {
    
    this.form.submit();
});