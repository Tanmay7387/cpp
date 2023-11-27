from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', RedirectView.as_view(url='/bank/dashboard/', permanent=True)),  # Redirect /bank/ to /bank/dashboard/
    path('dashboard/', views.dashboard, name='dashboard'),
    # Removed deposit and withdraw paths since they are handled in dashboard
    # Add login and logout URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_request, name='register'),
]
