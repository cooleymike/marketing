from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import path
from django.utils.timezone import now
from core.models import Employee, Receipt, ExpenseType, Sum, Team, FundRequest
from .models import ProjectEmployeeAllocatedBudget, Expense, Project



@login_required
def expense_list_by_quarter(request):
    # Ensure the user is a manager
    if not request.user.groups.filter(name='Manager').exists():
        return HttpResponseForbidden("You are not authorized to view this page.")

    # Get the active project for the logged-in manager
    allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(employee=request.user, is_active=True).first()
    if not allocated_budget_record:
        return HttpResponseForbidden("You do not have an active project.")

    project = allocated_budget_record.project
    # Get the expenses of the team the manager is in charge of
    print(request.user)
    team_managed = Team.objects.filter(manager="user")  # Assuming `Team` has a `manager` field
    expenses = Expense.objects.filter(team__in=team_managed,
                                      project_id=project.id)
    # Get the current year and quarter
    current_year = now().year
    current_quarter = (now().month - 1) // 3 + 1

    # Filter expenses by the project and current year/quarter
    expenses = Expense.objects.filter(project=project, created_date__year=current_year, created_date__quarter=current_quarter)

    total_expense = expenses.aggregate(total=Sum('initial_amount'))['total'] or 0

    context = {
        'expenses': expenses,
        'total_expense': total_expense,
        'current_year': current_year,
        'current_quarter': current_quarter,
        'project': project,
    }

    return render(request, 'admin/admin_expense_viewer.html', context)


# Register custom admin view
class CustomAdminSite(admin.AdminSite):
    site_header = "Expense Management Admin"
    site_title = "Admin"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('admin_expense_viewer/', expense_list_by_quarter,
                 name='admin_expense_viewer'),
        ]
        return custom_urls + urls


admin_site = CustomAdminSite(name='custom_admin')


class ProjectEmployeeAllocatedAmountAdmin(admin.ModelAdmin):
    list_display = ['employee', 'project', 'allocated_budget']
    search_fields = ['employee__username', 'project__name']


admin.site.register(ProjectEmployeeAllocatedBudget)
admin.site.register(Project)
admin.site.register(ExpenseType)
# admin.site.register(Project, EmployeeAdmin, Employee)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["description", "initial_amount", "created_date",
                    "employee"]

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(FundRequest)


class EmployeeAdmin(UserAdmin):
    list_display = ["username", "email",  "account_number","avatar","team"]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    form = UserChangeForm
    fieldsets = (
        (None, {
            'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')}),
        ('Groups', {
            'fields': ('groups',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'team',
                       'user_permissions')}),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')}),
    )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': (
    #         'username', 'first_name', 'last_name', 'email', 'password1',
    #         "password2", "team")}
    #      ),
    # )

admin.site.register(Team)
admin.site.register(Employee, EmployeeAdmin)

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ["created_date", "amount", "description", "expense"]

admin.site.register(Receipt, ReceiptAdmin)




