from django.contrib import admin
from core.models import Expense, Employee, Receipt
from .models import ProjectEmployeeAllocatedBudget, Expense, Project




class ProjectEmployeeAllocatedAmountAdmin(admin.ModelAdmin):
    list_display = ['employee', 'project', 'allocated_budget']
    search_fields = ['employee__username', 'project__name']


admin.site.register(ProjectEmployeeAllocatedBudget)
admin.site.register(Project)






class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["description", "initial_amount", "created_date",
                    "employee"]

admin.site.register(Expense, ExpenseAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["email", "username", "account_number"]

admin.site.register(Employee, EmployeeAdmin)

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ["created_date", "amount", "description", "expense"]

admin.site.register(Receipt, ReceiptAdmin)




