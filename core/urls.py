from logging import Manager

from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.generic import TemplateView

from core.views import ExpenseListView, ContactView, RegisterView, RequestFundsView, ManagerDashboardView, \
    ActiveProjectView, SettingsView, ExpenseFormView, TeamExpenseView
from .import views
from core.forms import CustomAuthenticationForm

urlpatterns = [
    # path('', views.homepage, name='homepage'),
    path('', TemplateView.as_view(template_name="home.html"), name='homepage'),
    path('expenses/',ExpenseListView.as_view(), name='expenses'),
    path('register/', RegisterView.as_view(), name='register'),
    path('signin/',LoginView.as_view(
        form_class=CustomAuthenticationForm,
        template_name='signin.html'
    ), name='signin'),
    path('team_expense/', TeamExpenseView.as_view(), name='team_expense'),
    path('employees_csv/', views.employee_csv, name='employees_csv'),
    path('expense_form/', ExpenseFormView.as_view(), name='expense_form'),
    path('active_project/', ActiveProjectView.as_view(), name='active_project'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
    path('request_funds/', RequestFundsView.as_view(), name='request_funds'),
    path('manager_dashboard/', ManagerDashboardView.as_view(), name='manager_dashboard'),
path(
    'manager/fund-request/<int:pk>/<str:decision>/',
    views.ApproveFundsView.as_view(),
    name='approve_funds_request'
)
]
