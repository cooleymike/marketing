
from django.urls import path, include
from payment.views import success, cancel, pricing_view

urlpatterns = [
    path('pricing/', pricing_view, name='pricing'),
    path('success/', success, name='success'),
    path('cancel/',cancel, name='cancel')
    ]