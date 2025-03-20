from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('blog/', views.blog, name='blog'),
    path('blog1/<int:article_id>/', views.blog1, name='blog1'),
    path('post-comment/', views.post_comment, name='post_comment'),
    path('noblog/', views.noblog, name='noblog'),
]