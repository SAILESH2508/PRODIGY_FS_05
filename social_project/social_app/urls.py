from django.urls import path
from . import views
from .views import PostCreateView # Import the class-based view
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Main Feed
    path('', views.feed_view, name='feed'), 
    
    # User Profiles
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    # Interactions
    path('post/<int:post_id>/like/', views.like_post_toggle, name='like_post_toggle'),
    path('post/<int:post_id>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('user/<str:username>/follow/', views.follow_user_toggle, name='follow_user_toggle'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='social_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]