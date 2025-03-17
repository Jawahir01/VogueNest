from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Comment


# Create your views here.
def index(request):
    """ A view to return the index page """
    context = {
        'profile': request.user
    }
    return render(request, 'home/index.html', context)

def blog(request):
    """ A view to return the blog page """
    return render(request, 'home/blog.html')

def blog1(request, article_id):
    """ A view to return the blog1 page """
    if not article_id:
        return redirect('blog') 
    
    comments = Comment.objects.filter(article_id=article_id, approved=True)
    
    context = {
        'article_id': article_id,
        'comments': comments
    }
    return render(request, 'home/blog1.html', context)

def post_comment(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        comment_text = request.POST.get('comment')
        
        if not comment_text.strip():
            messages.error(request, "Comment cannot be empty!")
            return redirect('blog1', article_id=article_id)
        
        # Save to database (create Comment model first)
        try:
            Comment.objects.create(
                user=request.user,
                article_id=article_id,
                text=comment_text
            )
            messages.success(request, "Comment posted successfully!")
        except Exception as e:
            messages.error(request, "Error posting comment")
        
        return redirect('blog1', article_id=article_id)
    
    return redirect('home')

def noblog(request):
    """ A view to return the noblog page """
    return render(request, 'home/noblog.html')

def contact(request):
    """ A view to return the contact page """
    return render(request, 'home/contact.html')

def thank_you(request):
    """ A view to return the thank_you page """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        context = {
            'name': name,
            'email': email,
            'message': message
        }
        return render(request, 'home/thank_you.html', context)
    return redirect('home')
        

