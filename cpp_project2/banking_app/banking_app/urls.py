# banking_app/banking_app/urls.py

from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bank/', include('bank.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Include the default auth urls
    path('logout/', LogoutView.as_view(), name='logout'),  # Custom logout path
    # ... other patterns
]
