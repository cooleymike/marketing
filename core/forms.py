from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, CharField, PasswordInput, Form

from core.models import Employee, Expense


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ['username', 'email', 'password1','password2']

class SigninForm(Form):
    username = CharField()
    password = CharField(max_length=32, widget=PasswordInput)


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'initial_amount', 'employee' ]

