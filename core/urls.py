
from django.urls import path
from .import views



urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('expenses/', views.ExpenseListView.as_view(), name='expenses'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),  # keep only this one
    path('team_expense/', views.team_expense_view, name='team_expense'),
    path('employees_csv/', views.employee_csv, name='employees_csv'),
    path('expense_form/', views.expense_form, name='expense_form'),
    path('active_project/', views.active_project, name='active_project'),
    path('settings/', views.settings, name='settings'),
    path('features/', views.features_view, name='features'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('contact/', views.contact_view, name='contact'),
    path('request_funds/', views.request_funds_view, name='request_funds'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
path(
    'manager/fund-request/<int:pk>/<str:decision>/',
    views.approve_funds_requests,
    name='approve_funds_request'
),
]
