from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.generic import TemplateView

from core.views import ExpenseListView, ContactView
from .import views
from core.forms import CustomAuthenticationForm

urlpatterns = [
    # path('', views.homepage, name='homepage'),
    path('', TemplateView.as_view(template_name="home.html"), name='homepage'),
    path('expenses/',ExpenseListView.as_view(), name='expenses'),
    path('register/', views.register, name='register'),
    path('signin/',LoginView.as_view(
        form_class=CustomAuthenticationForm,
        template_name='signin.html'
    ), name='signin'),
    path('team_expense/', views.team_expense_view, name='team_expense'),
    path('employees_csv/', views.employee_csv, name='employees_csv'),
    path('expense_form/', views.expense_form, name='expense_form'),
    path('active_project/', views.active_project, name='active_project'),
    path('settings/', views.settings, name='settings'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
    path('request_funds/', views.request_funds_view, name='request_funds'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
path(
    'manager/fund-request/<int:pk>/<str:decision>/',
    views.approve_funds_requests,
    name='approve_funds_request'
)
]
