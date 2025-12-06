# social_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🌟 Include Django's built-in Authentication URLs
    # Provides: /accounts/login/, /accounts/logout/, /accounts/password_change/, etc.
    path('accounts/', include('django.contrib.auth.urls')),

    # 🌟 Include your social app's URLs (home feed, profiles, register, etc.)
    path('', include('social_app.urls')),
]
