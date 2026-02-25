from django.contrib.auth.views import LoginView
from django.urls import path, include
from .import views
from core.forms import CustomizeSigninForm


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),  # keep only this one
    path('team_expense/', views.team_expense_view, name='team_expense'),
    path('employees/csv/', views.employee_csv, name='employee_csv'),
    path('expense_form/', views.expense_form, name='expense_form'),
    path('active_project/', views.active_project, name='active_project'),
    path('settings/', views.settings, name='settings'),
    path('admin_expense_viewer/', views.admin_expense_viewer, name='admin_expense_viewer'),
    path('features/', views.features_view, name='features'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('contact/', views.contact_view, name='contact'),
    path('request_funds/', views.request_funds_view, name='request_funds'),
]














