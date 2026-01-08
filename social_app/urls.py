from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import PostCreateView

urlpatterns = [
    # Auth
    path('accounts/login/', auth_views.LoginView.as_view(template_name='social_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),

    # Password Reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    
    # Password Change
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    # Main Feed
    path('', views.feed_view, name='feed'), 
    path('following/', views.following_feed_view, name='following_feed'), 
    
    # User Profiles
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('settings/profile/', views.profile_update_view, name='profile_update'),
    path('profile/update/', views.profile_update_view), # Compatibility redirect
    path('search/', views.search_view, name='search'),
    
    # Posts
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/pin/', views.toggle_pin_post, name='toggle_pin_post'),
    
    # Interactions
    path('post/<int:post_id>/like/', views.like_post_toggle, name='like_post_toggle'),
    path('post/<int:post_id>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:comment_id>/reply/', views.add_reply_to_comment, name='add_reply_to_comment'),
    path('user/<str:username>/follow/', views.follow_user_toggle, name='follow_user_toggle'),
    
    # Hashtags
    path('hashtag/<str:hashtag_name>/', views.hashtag_view, name='hashtag_view'),
    
    # Notifications
    path('notifications/', views.notifications_view, name='notifications'),
    path('api/notifications/unread-count/', views.unread_notifications_count, name='unread_notifications_count'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)