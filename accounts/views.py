from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('homepage')


