from django.forms import ModelForm, CharField, PasswordInput
from core.models import Employee
from django.contrib.auth.models import User

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class CreateEmployeeForm(ModelForm):
    password_check = CharField(widget= PasswordInput())
    password = CharField(widget= PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

