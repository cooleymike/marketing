from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.forms import (
    ModelForm, CharField, PasswordInput, Form,
    HiddenInput, ModelChoiceField, TextInput,
    DecimalField, NumberInput, ImageField, FileInput
)
from core.models import Employee, Expense, ProjectEmployeeAllocatedBudget, \
    ExpenseType
from django import forms
from .models import FundRequest

class FundRequestForm(forms.ModelForm):
    class Meta:
        model = FundRequest
        fields = ['project', 'amount_requested', 'quarter', 'justification']
        widgets = {
            'project': forms.Select(attrs={
                'class': 'w-full p-4 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white'
            }),
            'amount_requested': forms.NumberInput(attrs={
                'placeholder': 'Amount Requested',
                'class': 'w-full p-4 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white'
            }),
            'quarter': forms.Select(attrs={
                'class': 'w-full p-4 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white'
            }),
            'justification': forms.Textarea(attrs={
                'placeholder': 'Justification',
                'rows': 4,
                'class': 'w-full p-4 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white'
            }),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    avatar = ImageField(
        required=False,
        widget=FileInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
    )
    class Meta:
        model = Employee
        fields = ['username', 'email', 'password1', 'password2','avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-input rounded-full'


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    avatar = ImageField(
        required=False,
        widget=FileInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
    )

    class Meta:
        model = Employee
        fields = ['username', 'email', 'password1', 'password2', 'avatar']


class SigninForm(Form):
    username = CharField(widget=TextInput(attrs={
        "class": "border p-3 w-full shadow-md rounded-lg dark:bg-indigo-700 dark:text-gray-300 dark:border-gray-700",
        "placeholder": "Username",
    }))
    password = CharField(widget=PasswordInput(attrs={
        "class": "border p-3 w-full shadow-md rounded-lg dark:bg-indigo-700 dark:text-gray-300 dark:border-gray-700",
        "placeholder": "Password",
    }))


class ExpenseForm(ModelForm):
    employee = ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=HiddenInput()
    )
    description = CharField(
        label='Description',
        max_length=100,
        widget=TextInput(attrs={
            'class': "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        })
    )

    initial_amount = DecimalField(
        label='Initial amount',
        widget=NumberInput(attrs={
            'class': "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        })
    )

    type = forms.ModelChoiceField(

         queryset=ExpenseType.objects.all(),
        widget=forms.Select(attrs={
            'class': "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        })
    )

    upload = ImageField(
        label='Upload',
        widget=FileInput(attrs={
            'class': "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        })
    )

    class Meta:
        model = Expense
        fields = ['employee', 'description', 'initial_amount', 'upload', 'type']

    def clean_initial_amount(self):
        employee = self.cleaned_data["employee"]
        allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
            is_active=True, employee=employee).first()

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

class CustomizeSigninForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
    })
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
    }),
    )



