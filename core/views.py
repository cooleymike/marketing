import csv
from decimal import Decimal

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, F
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, FormView, CreateView, UpdateView, DeleteView

from core.tasks import send_contact_email

from EP.settings import RECIPIENT_EMAIL, DEFAULT_FROM_EMAIL
from core.models import Expense, ProjectEmployeeAllocatedBudget, Team, Employee, FundRequest, Project
from .forms import ExpenseForm, CreateUserForm, SigninForm, RegisterForm, FundRequestForm, ContactForm
from django.utils import timezone

def testimonials_view(request):
    return render(request, "testimonials.html")

def pricing_view(request):
    return render(request, "pricing.html")

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        #format the message
        full_message = f"Message from {name} <{email}>:\n\n{message}"
        send_contact_email.delay(
            subject='New Contact Message',
            message=full_message,
            recipient_list=[RECIPIENT_EMAIL]
        )
    #send mail remains the same!
        # send_mail(
        #     subject='New Contact Message',
        #     message=full_message,
        #     from_email=DEFAULT_FROM_EMAIL,  # Use configured sender
        #     recipient_list=[RECIPIENT_EMAIL],
        #          )
        messages.success(self.request, "Thanks for your message! We'll be in touch.")
        return super().form_valid(form)

class RequestFundsView(LoginRequiredMixin, CreateView):
    model = FundRequest
    form_class = FundRequestForm
    template_name = 'request_funds.html'
    success_url = reverse_lazy('request_funds')

    def form_valid(self, form):
        form.instance.employee = self.request.user
        messages.success(self.request, "Thanks for your request!")
        return super().form_valid(form)


def is_manager(user):
    return getattr(user, "is_manager", False)

class ManagerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'manager_dashboard.html'
    login_url = reverse_lazy('manager_signin')
    success_url = reverse_lazy('manager_dashboard')

    def test_func(self):
        return is_manager(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        managed_projects = Project.objects.filter(manager=self.request.user)
        context['pending_requests'] = FundRequest.objects.filter(
            status='pending',
            projects__in=managed_projects,
        )
        return context
#
# @user_passes_test(is_manager, login_url='manager_singin')
# def manager_dashboard(request):
#     managed_teams = Team.objects.filter(manager=request.user)
#     managed_projects = Project.objects.filter(teams__in=managed_teams)
#     pending_requests = FundRequest.objects.filter(
#         status="Pending",
#         project__in=managed_projects,
#     )
#
#     context = {
#         'pending_requests': pending_requests,
#     }
#     return render(request, "manager_dashboard.html", context)
class ApproveFundsView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model = FundRequest
    fields = []
    success_url = reverse_lazy('request_funds')

    def test_func(self):
        return is_manager(self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        decision = self.kwargs.get('decision')

        if decision == 'approve':
            self.object.status = 'Approved'
        elif decision == 'deny':
            self.object.status = 'rejected'
        else:
            messages.error(self.request, "Invalid decision.")
            return redirect('manager_dashboard')

        self.object.reviewer = self.request.user
        self.object.reviewed_at = timezone.now()
        self.object.save()
        messages.success(self.request, f"Request {decision}d.")
        return redirect('manager_dashboard')

    def get_object(self):
        return get_object_or_404(FundRequest, pk=self.kwargs['pk'])

# @user_passes_test(is_manager, login_url='manager_signin')
# def approve_funds_requests(request, pk, decision):
#     if request.method != 'POST':
#         return redirect('manager_dashboard')  # Change this
#
#     fund_request = get_object_or_404(FundRequest, pk=pk, status="Pending")
#
#     if decision == "approve":
#         fund_request.status = "Approved"
#         fund_request.save()
#     elif decision == "reject":
#         fund_request.status = "Rejected"
#     else:
#         messages.error(request, "Not a valid decision.")
#         return redirect('manager_dashboard')
#
#     fund_request.reviewer = request.user
#     fund_request.reviewed_at = timezone.now()
#     fund_request.save()
#     messages.success(request, f"Request {decision}d.")
#     return redirect("manager_dashboard")  # Change this too

class ExpanseListByQuarterView(LoginRequiredMixin, ListView):
    template_name = 'admin_expense_viewer.html'
    login_url = reverse_lazy('signin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenses'] = Expense.objects.filter(
            employee=self.request.user).order_by('-created_date')
        return context

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = "expenses.html"
    ordering = ['-created_date']

    def get_queryset(self):
        user = self.request.user
        current_team=user.team
        expenses= Expense.objects.filter(
            team=current_team,
        ).order_by('-created_date')

        return expenses

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user

        current_allocated_budget = ProjectEmployeeAllocatedBudget.objects.filter(
            is_active=True, employee=user
        ).first()

        if current_allocated_budget is None:
            messages.error(self.request, "You don't have any allocated budget.")
            return context_data

        expenses = Expense.objects.filter(employee=user)
        emp_total = expenses.aggregate(total=Sum("initial_amount"))["total"] or 0

        # Calculate remaining budget and percentage
        remaining_budget = current_allocated_budget.allocated_budget - emp_total
        percentage_left = (
            (remaining_budget / current_allocated_budget.allocated_budget) * 100
            if current_allocated_budget.allocated_budget else 0
        )

        # Build pie chart data
        datapoints = [
            {
                "y": round(float(emp_total), 2),
                "label": "Spent",
                "color": "#9b0808"
            },
            {
                "y": round(float(remaining_budget), 2),
                "label": "Remaining",
                "color": "#075c49"
            }
        ]

        # Build context
        context_data.update({
            "emp_total": emp_total,
            "remaining_budget": remaining_budget,
            "allocated_budget": current_allocated_budget.allocated_budget,
            "percentage_left": round(percentage_left, 2),
            "active_quarter": current_allocated_budget.quarter,
            "datapoints": datapoints,  # Pass to template
        })

        return context_data


class RegisterView(CreateView):
    model = Employee
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password1'])
        messages.success(self.request, "Registration successful")
        return super().form_valid(form)


# def register(request):
#    if request.method == 'POST':
#         form = RegisterForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             form.instance.set_password(form.cleaned_data['password1'])
#             form.save()
#             messages.success(request, "Registration successful")
#             return redirect('homepage') # redirect to signin or maybe home
#
#    else:
#         form = RegisterForm()
#
#    return TemplateResponse(request,'register.html',
#                             {"form":form})

from calendar import month_name

@login_required
def team_expense_view(request):
    quarter = int(request.GET.get('quarter', 0))
    month = int(request.GET.get('month', 0))

    allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
        employee=request.user, is_active=True).first()

    if not allocated_budget_record:
        messages.error(request, "You are not part of any active project.")
        return redirect('homepage')

    project = allocated_budget_record.project
    project_users = ProjectEmployeeAllocatedBudget.objects.filter(
        project=project, is_active=True
    ).select_related('employee')

    # Get all expenses for the project
    expenses = Expense.objects.filter(project=project)

    # Apply filters if selected
    if quarter:
        expenses = expenses.filter(created_date__quarter=quarter)
    if month:
        expenses = expenses.filter(created_date__month=month)

    expenses = expenses.order_by('-created_date')

    # Calculate totals
    total_spent_all = expenses.aggregate(total=Sum("initial_amount"))["total"] or Decimal('0.00')
    total_budget_all = project_users.aggregate(total=Sum('allocated_budget'))["total"] or Decimal('0.00')
    remaining_all = total_budget_all - total_spent_all
    remaining_pct = round((remaining_all / total_budget_all * 100), 2) if total_budget_all else 0

    team_expenses = []
    for record in project_users:
        employee_expenses = expenses.filter(employee=record.employee)
        emp_total = employee_expenses.aggregate(total=Sum('initial_amount'))['total'] or Decimal('0.00')
        budget_used_pct = (emp_total / record.allocated_budget * 100) if record.allocated_budget else Decimal('0.00')

        # Set color status
        if budget_used_pct >= 90:
            color = 'red'
        elif budget_used_pct >= 70:
            color = 'yellow'
        else:
            color = 'green'

        team_expenses.append({
            'name': f"{record.employee.first_name} {record.employee.last_name}",
            'allocated_budget': emp_total,
            'budget_used_pct': round(budget_used_pct, 2),
            'status_color': color,
        })

    context = {
        'expenses': expenses,
        'project': project,
        'team_expenses': team_expenses,
        'selected_quarter': quarter,
        'selected_month': month,
        'months': list(enumerate(month_name))[1:],
        'quarters': [1, 2, 3, 4],
        'total_spent_all': total_spent_all,
        'total_budget_all': total_budget_all,
        'remaining_all': remaining_all,
        'remaining_pct': remaining_pct,
    }
    return render(request, 'team_expense.html', context)


@login_required
def employee_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    team_employee = Employee.objects.filter(
        team=request.user.team
    ).filter(
        projectemployeeallocatedbudget__is_active=True
    ).annotate(
        total_spent=Sum("expense__initial_amount"),
        allocated_budget=F("projectemployeeallocatedbudget__allocated_budget"),
        project_name=F("projectemployeeallocatedbudget__project__name"),
    ).annotate(
        remaining_budget=F("allocated_budget") - F("total_spent")
    ).annotate(
        percentage_left=((F("remaining_budget") / F("allocated_budget")) * 100)
    )

    fieldnames = ['username', 'project_name', 'total_spent', 'percentage_left', "allocated_budget", "remaining_budget"]
    selected_values=team_employee.values(*fieldnames)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(selected_values)

    return response


class ExpenseFormView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense_form.html'
    success_url = reverse_lazy('homepage')

    def get(self, request, *args, **kwargs):
        allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
            employee=request.user, is_active=True).first()

        if allocated_budget_record is None:
            messages.error(request, "You are not part of any active project.")
            return redirect('homepage')

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
            employee=request.user, is_active=True).first()

        if allocated_budget_record is None:
            messages.error(request, "You are not part of any active project.")
            return redirect('homepage')

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
            employee=self.request.user, is_active=True).first()

        project_id = allocated_budget_record.project_id
        active_entry = Expense.objects.filter(employee=self.request.user, project_id=project_id)
        emp_total = active_entry.aggregate(total=Sum('initial_amount'))['total'] or 0
        total_budget = allocated_budget_record.allocated_budget if allocated_budget_record else 0
        remaining_budget = total_budget - emp_total

        context['active_entry'] = active_entry
        context['total_expense'] = emp_total
        context['remaining_budget'] = remaining_budget

        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['employee'] = self.request.user
        initial['team'] = self.request.user.team
        return initial

    def form_valid(self, form):
        allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
            employee=self.request.user, is_active=True).first()

        if not allocated_budget_record:
            messages.error(self.request, "You do not have an allocated budget for this project.")
            return redirect('homepage')

        expense_to_save = form.save(commit=False)
        expense_to_save.employee = self.request.user
        expense_to_save.project_id = allocated_budget_record.project_id
        expense_to_save.save()

        messages.success(self.request, "Expense recorded successfully.")
        return super().form_valid(form)


# @login_required
# def expense_form(request):
#     print("***")
#     print(request.FILES)
#     print("---")
#     # Get the project ID from the request or default to 1
#     #project_id = request.GET.get('project_id', 1)
#
#     # Fetch allocated budget for the project
#     allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
#         employee=request.user, is_active=True).first()
#
#     if allocated_budget_record is None:
#         messages.error(request, "You are not part of any active project.")
#         return redirect('homepage')
#
#     project_id = allocated_budget_record.project_id
#     if request.method == 'POST':
#         print(request.POST)
#         form = ExpenseForm(request.POST, request.FILES)
#         if form.is_valid():
#
#             if not allocated_budget_record:
#                 messages.error(request,
#                                "You do not have an allocated budget for this project.")
#                 return redirect('homepage')  # or another appropriate page
#             print(form.cleaned_data)
#             expense_to_save = form.save(commit=False)
#             expense_to_save.employee = request.user
#             expense_to_save.project_id = project_id # this sets the project id
#             print(expense_to_save.type)
#             expense_to_save.save()
#             messages.success(request, "Expense recorded successfully.")
#             return redirect('homepage')  # Redirect to the same page or
#             # another page
#         else:
#             print(form.errors)
#     else:
#         form = ExpenseForm(initial={
#
#             "employee": request.user,
#             "team": request.user.team
#         })
#     # For GET request
#     active_entry = Expense.objects.filter(employee=request.user,
#                                           project_id=project_id)
#     emp_total = active_entry.aggregate(total=Sum('initial_amount'))[
#                       'total'] or 0
#
#     total_budget = allocated_budget_record.allocated_budget if (
#         allocated_budget_record) else 0
#     remaining_budget = total_budget - emp_total
#
#     context = {
#         'form': form,
#         'active_entry': active_entry,
#         'total_expense': emp_total,
#         'remaining_budget': remaining_budget
#     }
#     return render(request, "expense_form.html", context)

def total_allocated_expense(request):
    total_expense = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, "expense.html", {'total_expense':
                                                                total_expense})
def project_list(request):
    return render(request, 'projects.html')
#make migrations, migrate

class ActiveProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'active_project.html'

    def get(self, request, *args, **kwargs):
        active_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
            employee=request.user, is_active=True).first()

        if not active_budget_record:
            messages.error(request, "You do not have an active budget")
            return redirect('homepage')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
            employee=self.request.user, is_active=True).first()
        active_project = active_budget_record.project
        expenses = Expense.objects.filter(employee=self.request.user, project=active_project)

        context['active_project'] = active_project
        context['expenses'] = expenses

        return context


# @login_required
# def active_project(request):
#     #here we find the active budget record
#     active_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
#         employee=request.user, is_active=True).first()
#     #check if active budget exists - this would be nice to have
#     if not active_budget_record:
#         messages.error(request, "You do not have an active budget")
#         return redirect('homepage')
#     #pull project from active budget record
#     active_project = active_budget_record.project
#     #fetch related expenses for current project
#     expenses = Expense.objects.filter(employee=request.user, project=active_project)
#     # here we render as always, passing the project and expenses
#     return render(request,
#       'active_project.html', {
#                     'active_project': active_project,
#                     'expenses': expenses
#     })

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Settings'
        return context

    def post(self, request, *args, **kwargs):
        if "delete account" in request.POST:
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('homepage')
        return super().get(request, *args, **kwargs)
# @login_required
# def settings(request):
#     if request.method == "POST":
#         if "delete_account" in request.POST:  # Check if the delete button was clicked
#             user = request.user
#             user.delete()
#             logout(request)
#             messages.success(request, "Your account has been deleted successfully.")
#             return redirect('homepage')  # Redirect to homepage after deletion
#
#         # Handle other POST actions here, such as updating user details
#     return TemplateResponse(request, "settings.html", {"title": "Settings"})

def privacy_policy(request):
    return render(request, "privacy_policy.html")

def terms_of_service(request):
    return render(request, "terms_of_service.html")

def custom_404(request, _exception):
    return render(request, '404.html', status=404)