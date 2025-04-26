from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from EP.views import expenses
from core.models import Expense, ProjectEmployeeAllocatedBudget, Team
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm, CreateUserForm, SigninForm, RegisterForm
from django.utils import timezone

def features_view(request):
    return render(request, "features.html")

def testimonials_view(request):
    return render(request, "testimonials.html")


@login_required
def admin_expense_viewer(request):
   if not request.user.is_staff: # needs to be a manager/staff
        return redirect('admin:index')  # Redirect to home if not manager

   team = request.user.team # managers team
   current_year = timezone.now().year
   expenses = Expense.objects.filter(team=team, created_date__year=current_year)


        # Group expenses by quarter
   admin_expense_viewer = {
        1: expenses.filter(created_date__quarter=1),
        2: expenses.filter(created_date__quarter=2),
        3: expenses.filter(created_date__quarter=3),
        4: expenses.filter(created_date__quarter=4),
    }

   return render(request, 'admin_expense_viewer.html', {
        'admin_expense_viewer': admin_expense_viewer,
        'current_year': current_year
    })
@login_required
def expense_list_by_quarter(request):
    # Your logic to filter and order expenses by year/quarter
    expenses = Expense.objects.filter(user=request.user).order_by('date')
    # Render the expenses template or return a custom response
    return render(request, 'admin/admin_expense_viewer.html', {'expenses':
                                                               expenses})



def homepage(request):
   return TemplateResponse(request, "home.html", {"title": "homepage"})

def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("homepage")
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = SigninForm()

    return TemplateResponse(request, "signin.html", {"form": form})

def expense_entry_view(request):
    form = ExpenseForm()

    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.instance.type)
            return redirect('expenses')  # Adjust to your actual URL name
        else:
            print(form.errors)

    return render(request, 'expenses.html', {'form': form})

@login_required
def expenses_view(request):
    user = request.user

    current_allocated_budget = ProjectEmployeeAllocatedBudget.objects.filter(
        is_active=True, employee=request.user).first()

    if current_allocated_budget is None:
        messages.info(request, "You have not been attached to any budget")
        print("User: ", request.user)
        print("Project ID:", current_allocated_budget)
        print("Expense found:", Expense.objects.filter(user=request.user,
                                                       project=current_allocated_budget).count())
        return redirect("homepage")
    project_id = current_allocated_budget.project_id
    budget = current_allocated_budget.budget
    allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
        employee=request.user, project_id=project_id, is_active=True
    ).first()


    total_spent = expenses.aggregate(total=Sum("initial_amount"))["total"] or 0
    remaining_budget = allocated_budget_record.allocated_budget - total_spent
    percentage_left = (
        (remaining_budget / allocated_budget_record.allocated_budget) * 100
        if allocated_budget_record.allocated_budget else 0
    )
    # pass these as context data from back to front 
    context = {
        "expenses": expenses,
        "total_spent": total_spent,
        "remaining_budget": remaining_budget,
        "allocated_budget": allocated_budget_record.allocated_budget,
        "percentage_left": round(percentage_left, 2),
        "active_quarter": allocated_budget_record.quarter,
        # this to show which quarter is active (i think)
    }

    return render(request,'expenses.html', {"expenses": expenses})

def register(request):
   if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.set_password(form.cleaned_data['password1'])
            form.save()
            messages.success(request, "Registration successful")
            return redirect('signin_view') # redirect to signin or maybe home

   else:
        form = RegisterForm()

   return TemplateResponse(request,'register.html',
                            {"form":form})


@login_required
def team_expense_view(request):
    # Identify the active project for the logged-in user
    allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
        employee=request.user, is_active=True
    ).first()

    if not allocated_budget_record:
        messages.error(request, "You are not part of any active project.")
        return redirect('homepage')

    project = allocated_budget_record.project

    # Fetch all users related to this project (e.g., via allocated budgets)
    project_users = ProjectEmployeeAllocatedBudget.objects.filter(
        project=project, is_active=True
    ).values('employee', 'employee__first_name', 'employee__last_name')

    # Calculate individual expenses for users in the project
    team_expenses = []
    for user in project_users:
        total_expenses = Expense.objects.filter(
            employee_id=user['employee'], project=project
        ).aggregate(total=Sum('initial_amount'))['total'] or 0

        team_expenses.append({
            'name': f"{user['employee__first_name']} {user['employee__last_name']}",
            'total_expenses': total_expenses,
        })

    # Prepare context for rendering
    context = {
        'project': project,
        'team_expenses': team_expenses,
    }

    return render(request, 'team_expense.html', context)


@login_required
def expense_form(request):
    print("***")
    print(request.FILES)
    print("---")
    # Get the project ID from the request or default to 1
    #project_id = request.GET.get('project_id', 1)

    # Fetch allocated budget for the project
    allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
        employee=request.user, is_active=True).first()

    if allocated_budget_record is None:
        messages.error(request, "You are not part of any active project.")
        return redirect('homepage')

    project_id = allocated_budget_record.project_id
    if request.method == 'POST':
        print(request.POST)
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():




            if not allocated_budget_record:
                messages.error(request,
                               "You do not have an allocated budget for this project.")
                return redirect('homepage')  # or another appropriate page
            print(form.cleaned_data)
            expense_to_save = form.save(commit=False)
            expense_to_save.employee = request.user
            expense_to_save.project_id = project_id # this sets the project id
            print(expense_to_save.type)
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
    return render(request, "expense.html", {'total_expense':
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


@login_required
def settings(request):
    if request.method == "POST":
        if "delete_account" in request.POST:  # Check if the delete button was clicked
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('homepage')  # Redirect to homepage after deletion

        # Handle other POST actions here, such as updating user details

    return TemplateResponse(request, "settings.html", {"title": "Settings"})



