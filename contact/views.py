from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import ContactSubmission

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save()

            return redirect('thank_you')
        
    else:
        form = ContactForm()

    context = {
        'form': form
        }
    template = 'contact/contact.html'
    return render(request, template, context)

def thank_you(request):
    template = 'contact/thank_you.html'
    return render(request, template)