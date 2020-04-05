"""AKADS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.landing, name='landing'),
    path('booking', user_views.booking, name='booking'),
    path('register/', user_views.tutor_tutee, name='register'),
    path('register/tutor/', user_views.register_tutor, name='register-tutor'),
    path('register/tutee/', user_views.register_tutee, name='register-tutee'),
    path('home/', user_views.home, name='home'),
    path('home/<int:session_id>/accepted', user_views.accept_tutee, name='accept'),
    path('home/<int:session_id>/delete', user_views.delete_request, name='delete'),
    path('login/', user_views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/landing.html'), name='logout'),
    path('home/upcoming', user_views.upcoming, name='upcoming'),
    path('home/unconfirmed', user_views.unconfirmed, name='unconfirmed'),
    path('home/unconfirmed/<int:session_id>/edit', user_views.unconfirmed_edit, name='unconfirmed_edit'),
    path('home/unconfirmed/<int:session_id>/<str:status>', user_views.unconfirmed_status, name='unconfirmed_status'),
    path('home/pending', user_views.pending, name='pending'),
    path('home/history', user_views.history, name='history'),
    path('home/<int:session_id>/complete-session', user_views.complete_session, name='complete_session'),
    path('home/pending/<int:session_id>/cancel', user_views.cancel_pending, name='cancel_pending'),
    path('transactions/', user_views.transactions, name='transactions'),
    path('pay/', user_views.pay_balance, name='pay_balance'),
    path('home/profile', user_views.profile, name='profile'),
    path('home/profile/password', user_views.edit_password, name='edit_password'),
    path('home/profile/location', user_views.edit_location, name='edit_location'),
    path('home/profile/resume', user_views.edit_resume, name='edit_resume'),
    path('home/profile/card', user_views.edit_card, name='edit_card'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
