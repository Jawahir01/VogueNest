// Initialize Stripe Elements
var stripePublicKey = JSON.parse(document.getElementById('id_stripe_public_key').textContent);
var clientSecret = JSON.parse(document.getElementById('id_client_secret').textContent);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var card = elements.create('card', {
    style: {
        base: {
            color: '#333',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    }
});

card.mount('#card-element');

// Handle real-time validation errors
card.addEventListener('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
        displayError.style.display = 'block';
    } else {
        displayError.textContent = '';
        displayError.style.display = 'none';
    }
});

// Handle form submission
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    document.getElementById('loading-overlay').style.display = 'block';
    
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: form.querySelector('#id_full_name').value,
                email: form.querySelector('#id_email').value
            }
        }
    }).then(function(result) {
        if (result.error) {
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
            errorElement.style.display = 'block';
            document.getElementById('loading-overlay').style.display = 'none';
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});

// Enable form validation
(function() {
    'use strict';
    window.addEventListener('load', function() {
        var forms = document.getElementsByClassName('needs-validation');
        Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();