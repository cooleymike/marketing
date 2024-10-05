
from django.urls import path
from .import views


urlpatterns = [

    path('', views.homepage, name='homepage'),
    path('expenses', views.expenses_view, name='expenses'),
    path('register', views.register, name='register'),
    path('signin/', views.signin, name="signin"), # best practice use name=' '
    path('team_expense/', views.team_expense, name='team_expense'),
    path('expense_form/', views.expense_form, name='expense_form'),
    path('active_project/', views.active_project, name='active_project')




    ]





