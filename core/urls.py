
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.homepage, name='homepage_view'),
    path('bookkeeping', views.bookkeeping, name='bookkeeping'),
    path('register', views.register, name='register'),
    path('confirm/', views.confirm, name='confirm'),
    path('upload/', views.upload, name="uplaod"),
    path('signin/', views.signin, name="signin"), # best practice use name=' '
    path('about/', views.about, name='about'),
    path('team_expense/', views.team_expense, name='team_expense'),


    path('expense_form/', views.expense_form, name='expense_form')


    #path('login/', views.login, name='login')
    ]





