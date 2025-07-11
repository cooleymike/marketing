from django.urls import path, include
from .import views
from django.contrib.auth import views as auth_views



from .views import logout_view

urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(
         template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('logout/', logout_view, name='logout'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('socials/', include('allauth.urls')),




]