
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.homepage), #homepage url (.com)
    path('bookkeeping/', views.bookkeeping),
    path('managing/', views.managing),
    path('confirm/', views.confirm),
    path('signup/', views.signup, name='signup'),
    path('upload/', views.upload),
    path('signin/', views.signin, name="login"), # best practice use name=' '
    path('about/', views.about, name='about'),
    path('team_expense/', views.team_expense, name='team_expense'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    # path('rest/confirm)' ?

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'),
         name='password_reset_complete'),

    path('expense_form/', views.expense_form, name='create_form')


    #path('login/', views.login, name='login')
    ]



