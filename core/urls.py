from django.contrib.auth.views import LoginView
from django.urls import path, include
from .import views
from core.forms import CustomizeSigninForm


urlpatterns = [

    path('', views.homepage, name='homepage',),
    path('expenses/', views.expenses_view, name='expenses'),
    path('register/', views.register, name='register'),
    path('signin/', LoginView.as_view(template_name="signin.html",form_class=CustomizeSigninForm),
         name="signin_view"),

    path('team_expense/', views.team_expense_view, name='team_expense'),
    path('expense_form/', views.expense_form, name='expense_form'),
    path('active_project/', views.active_project, name='active_project'),
    path('settings/', views.settings, name='settings')



    ]





