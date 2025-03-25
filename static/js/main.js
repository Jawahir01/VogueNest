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

// Create BackTop Button
if (!document.getElementById('backToTopContainer')) {
    const container = document.createElement('div');
    container.id = 'backToTopContainer'; // Unique ID for container
    container.innerHTML = `
      <button class="btn btn-primary rounded-circle shadow">
        <i class="fas fa-arrow-up"></i>
      </button>
    `;
    container.style.display = 'none'; // Hidden initially
    container.style.transition = '0.3s'; // Set transition once
    document.body.appendChild(container);
  
    // Scroll handler
    window.addEventListener('scroll', () => {
      container.style.display = window.scrollY > 300 ? 'block' : 'none';
    });
  
    // Click handler
    container.querySelector('button').addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

// Product Image Zoom
document.querySelectorAll('.product-image').forEach(image => {
    image.addEventListener('click', function() {
        this.classList.toggle('zoomed');
    });
});

// Blog Card Hover Effect
document.querySelectorAll('.blog-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
})
});