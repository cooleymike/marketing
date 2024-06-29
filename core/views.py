from django.http import request
from django.shortcuts import render
from django.template.response import TemplateResponse


from core.models import Expense
from .forms import CreateEmployeeForm

def homepage(request):
   return TemplateResponse(request, "home.html", {"title": "homepage"})

def signin(request):
    return TemplateResponse(request, 'registration/login.html', {"title":
                                                                  "signin"})

def bookkeeping(request):
    print(Expense.objects.all())
    expenses = Expense.objects.filter(employee__username='JackJones')
    return TemplateResponse(request,'bookkeeping.html', {"expenses": expenses})

# registration and login part




def managing(request):
    return TemplateResponse(request,'managing.html', {"title": "managing"})

def confirm(request):
    return TemplateResponse(request,'confirm.html', {"title": "confirm"})

def signup(request):
    if request.method == 'POST':
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CreateEmployeeForm()
    return TemplateResponse(request,'registration/register.html',
                            {"form":form})


def upload(request):
   return TemplateResponse(request, "upload.html", {"title": "upload"})

def about(request):
   return TemplateResponse(request, "about.html", {"title": "about"})


def team_expense(request):
    return TemplateResponse(request, "team_expense.html", {"title": "team_expense"})


def expense_form(request):
    return render(request, '/team_expenses/expense_form.html')