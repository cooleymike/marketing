from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from core.models import Expense, ProjectEmployeeAllocatedBudget
from .forms import ExpenseForm, CreateUserForm, SigninForm, RegisterForm


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



def expenses_view(request):
    current_allocated_budget = ProjectEmployeeAllocatedBudget.objects.filter(
        is_active=True, employee=request.user).first()
    #if current allocated budget is none then redirect to homepage with
    # message you have not been attached to an allocated budget
    if current_allocated_budget is None:
        messages.error(request, "You have not been attached to any budget")
        return redirect("homepage")
    project_id = current_allocated_budget.project_id

    expenses = Expense.objects.filter(employee=request.user, project_id=project_id)


    return render(request,'expenses.html', {"expenses": expenses})

def register(request):
   if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.instance.set_password(form.cleaned_data['password1'])
            form.save()
            messages.success(request, "Registration successful")
            return redirect('signin_view') # redirect to signin or maybe home

   else:
        form = RegisterForm()

   return TemplateResponse(request,'register.html',
                            {"form":form})

def team_expense(request):
    return TemplateResponse(request, "team_expense.html", {"title": "team_expense"})


@login_required
def expense_form(request):
    # Get the project ID from the request or default to 1
    #project_id = request.GET.get('project_id', 1)

    # Fetch allocated budget for the project
    allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
        employee=request.user, is_active=True).first()

    project_id = allocated_budget_record.project_id
    if request.method == 'POST':
        print(request.POST)
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():


            if not allocated_budget_record:
                messages.error(request,
                               "You do not have an allocated budget for this project.")
                return redirect('homepage')  # or another appropriate page

            expense_to_save = form.save(commit=False)
            expense_to_save.employee = request.user
            expense_to_save.project_id = project_id # this sets the project id

            expense_to_save.save()
            messages.success(request, "Expense recorded successfully.")
            return redirect('homepage')  # Redirect to the same page or
            # another page
        else:
            print(form.errors)
    else:
        form = ExpenseForm(initial={
            "employee": request.user

        })

    # For GET request

    active_entry = Expense.objects.filter(employee=request.user,
                                          project_id=project_id)
    total_spent = active_entry.aggregate(total=Sum('initial_amount'))[
                      'total'] or 0

    total_budget = allocated_budget_record.allocated_budget if (
        allocated_budget_record) else 0
    remaining_budget = total_budget - total_spent

    context = {
        'form': form,
        'active_entry': active_entry,
        'total_expense': total_spent,
        'remaining_budget': remaining_budget
    }

    return render(request, "expense_form.html", context)


def total_allocated_expense(request):

    total_expense = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, "expenses.html", {'total_expense':
                                                                total_expense})
def project_list(request):

    return render(request, 'projects.html')
#make migrations, migrate

@login_required
def active_project(request):
    #here we find the active budget record
    active_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
        employee=request.user, is_active=True).first()

    #check if active budget exists - this would be nice to have
    if not active_budget_record:
        messages.error(request, "You do not have an active budget")
        return redirect('homepage')

    #pull project from active budget record
    active_project = active_budget_record.project

    #fetch related expenses for current project
    expenses = Expense.objects.filter(employee=request.user, project=active_project)

    # here we render as always, passing the project and expenses
    return render(request,
      'active_project.html', {
                    'active_project': active_project,
                    'expenses': expenses
    })



