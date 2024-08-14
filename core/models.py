from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    account_number = models.CharField(max_length=10, unique=True)

class Expense(models.Model):
    created_date = models.DateTimeField(auto_now_add=True,)
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    def __str__(self):
        return self.description + " " + self.employee.account_number


class Receipt(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)




