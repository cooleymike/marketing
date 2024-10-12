from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.forms import (
    ModelForm, CharField, PasswordInput, Form,
    HiddenInput, ModelChoiceField, TextInput,
    DecimalField, NumberInput, ImageField, FileInput
)
from core.models import (
    Employee, Expense,
    ProjectEmployeeAllocatedBudget
)


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
    employee = ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=HiddenInput()
    )
    description = CharField(
        label='Description',
        max_length=100,
        widget=TextInput(
            attrs={
                'class': (
                    "shadow appearance-none"
                    "border rounded w-full py-2 "
                    "px-3 text-gray-700" 
                    "leading-tight focus:outline-none"
                    "focus:shadow-outline"
                )
            }
        )
    )

    initial_amount = DecimalField(
        label='Initial amount',
        widget=NumberInput(
            attrs={
                'class': (
                    "shadow appearance-none "
                    "border rounded w-full py-2 "
                    "px-3 text-gray-700 "
                    "leading-tight "
                    "focus:outline-none focus:shadow-outline"
                )
            }
        )
    )

    upload = ImageField(
        label='Upload',
        widget=FileInput(
            attrs={
                'class': (
                    "shadow appearance-none "
                    "border rounded w-full py-2 "
                    "px-3 text-gray-700 "
                    "leading-tight "
                    "focus:outline-none focus:shadow-outline"
                )
            }
        )
    )



    class Meta:
        model = Expense
        # must put employee first with initial_amount or else you will not
        # have employee validated
        fields = ['employee','description','initial_amount',
                  'upload'
        ] # form
        # has
        # ability to convert string to in,
    def clean_initial_amount(self):


        # Extract the user authenticated from the form to find the allocated
        # budget for this user and the project passed in the url
        employee = self.cleaned_data["employee"]
        allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
            is_active=True, employee=employee).first()


        #TODO: Put this logic in a function in a utils file to be reusable
        # here and in views.py l.115 in the views.py
        previous_user_expenses_for_project = Expense.objects.filter(
            employee=employee,
            project=allocated_budget_record.project
        )

        total_spent = previous_user_expenses_for_project.aggregate(
            total=Sum('initial_amount'))['total'] or 0


        total_budget = allocated_budget_record.allocated_budget if (
            allocated_budget_record) else 0

        remaining_budget = total_budget - total_spent

        initial_amount = self.cleaned_data["initial_amount"]
        if initial_amount > remaining_budget:
            raise ValidationError('This amount is over the budget')
        return initial_amount




