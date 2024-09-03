from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from core.models import Expense
from .forms import ExpenseForm, CreateUserForm, SigninForm


def homepage(request):
   return TemplateResponse(request, "home.html", {"title": "homepage"})

def signin(request):
    if request.method == "POST":
        signinform = SigninForm(request.POST)
        if signinform.is_valid():
            username = signinform.cleaned_data["username"]
            password = signinform.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("homepage")
            else:
                messages.error(request, "Invalid username or password")

    else:
        signinform = SigninForm()

    return TemplateResponse(request, "signin.html", {"signinform": signinform})


@login_required
def expenses_view(request):
    expenses = Expense.objects.filter(employee=request.user)
    # for expense in expenses:
    #     expense.remaining_budget = expense.remaining_budget
    return render(request,'expenses.html', {"expenses": expenses})


# registration and login part



def confirm(request):
    return TemplateResponse(request,'confirm.html', {"title": "confirm"})

def register(request):
   if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful")
            return redirect('signin_view') # redirect to signin or maybe home

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

@login_required
def expense_form(request):
    total_budget = 10000

    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data)
            expense_to_save = form.save(commit=False) #save data, return saved obj.
            expense_to_save.employee = request.user #auth. user for this expense
            expense_to_save.save()
        else:
            print(form.errors)

    else:
        form = ExpenseForm()
    print(request.user)
    active_entry = Expense.objects.filter(employee=request.user)
    total_spent = (active_entry.aggregate(total=Sum('initial_amount'))['total'] or 0)
    remaining_budget = total_budget - total_spent

    context = {
        'form': form,
        'active_entry': active_entry,
        'total_expense':total_spent,
        'remaining_budget': remaining_budget
    }

    return render(request, "expense_form.html", context)

def total_allocated_expense(request):

    total_expense = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, "expenses.html", {'total_expense':
                                                                total_expense})


