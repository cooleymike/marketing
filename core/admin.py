from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from core.models import Expense, Employee, Receipt
from .models import ProjectEmployeeAllocatedBudget, Expense, Project


class ProjectEmployeeAllocatedAmountAdmin(admin.ModelAdmin):
    list_display = ['employee', 'project', 'allocated_budget']
    search_fields = ['employee__username', 'project__name']


admin.site.register(ProjectEmployeeAllocatedBudget)
admin.site.register(Project)
# admin.site.register(Project, EmployeeAdmin, Employee)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["description", "initial_amount", "created_date",
                    "employee"]

admin.site.register(Expense, ExpenseAdmin)


class EmployeeAdmin(UserAdmin):
    list_display = ["email", "username", "account_number"]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    # form = UserChangeForm

admin.site.register(Employee, EmployeeAdmin)

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ["created_date", "amount", "description", "expense"]

admin.site.register(Receipt, ReceiptAdmin)




