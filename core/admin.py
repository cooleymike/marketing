from django.contrib import admin
from core.models import Expense, Employee, Receipt

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




