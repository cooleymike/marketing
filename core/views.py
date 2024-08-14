from django.http import request
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login

from core.models import Expense
from .forms import ExpenseForm, CreateUserForm, SigninForm


def homepage(request):
   return TemplateResponse(request, "home.html", {"title": "homepage"})

def signin(request):
    print("valid")
    if request.method == "POST":
        signinform = SigninForm(request.POST)
        print(signinform)
        request.POST.get('username')
        request.POST.get('password')



        if signinform.is_valid():

            print("it's valid")

            user = authenticate(username=request.POST.get('username'),
                                    password=request.POST.get('password'))
            print(request.POST.get('username'), request.POST.get(
                'password'))

            if user is not None:
                login(request, user)
                return redirect('homepage_view')
            print(user)


    else:
        signinform = SigninForm()



    return TemplateResponse(request, "signin.html", {"signinform": signinform})


def bookkeeping(request):
    print(Expense.objects.all())
    expenses = Expense.objects.filter(employee__username='JackJones')
    return TemplateResponse(request,'bookkeeping.html', {"expenses": expenses})

# registration and login part



def confirm(request):
    return TemplateResponse(request,'confirm.html', {"title": "confirm"})

def register(request):

    if request.method == 'POST':
        request.POST.get('username')
        request.POST.get('password')



        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
        print(form.errors)
    else:
        form = CreateUserForm()
    return TemplateResponse(request,'register.html',
                            {"form":form})


def upload(request):
   return TemplateResponse(request, "upload.html", {"title": "upload"})

def about(request):
   return TemplateResponse(request, "about.html", {"title": "about"})


def team_expense(request):
    return TemplateResponse(request, "team_expense.html", {"title": "team_expense"})


def expense_form(request):
    form = ExpenseForm()
    return render(request, "expense_form.html", {"form":form})



