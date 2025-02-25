from django.shortcuts import render

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


