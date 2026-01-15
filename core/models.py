from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum


class Employee(AbstractUser):
    account_number = models.CharField(max_length=10, unique=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    team = models.ForeignKey("Team", null=True, on_delete=models.PROTECT, blank=True )

class Project(models.Model):
    description = models.CharField(max_length=150)
    name = models.CharField(max_length=50)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)  # total budget for the project
    due_date = models.DateField()

    def __str__(self):
        return self.name

    def total_allocated_budget(self):
        """ Sum of all employee budget allocations for this project """
        return self.allocated_budgets.aggregate(total=Sum('allocated_budget'))['total'] or 0


class ProjectEmployeeAllocatedBudget(models.Model):
    QUARTERS = [
        ('Q1', 'Q1(Jan-Mar)'),
        ('Q2', 'Q2 (Apr-Jun'),
        ('Q3', 'Q3 (Jul-Sep'),
        ('Q4', 'Q4 (Oct-Dec)'),
    ]

    QUARTER_MONTHS = {
        'Q1':[1,2,3],
        'Q2':[4,5,6],
        'Q3':[7,8,9],
        'Q4':[10,11,12],
    }


    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='allocated_budgets', on_delete=models.CASCADE)
    quarter = models.CharField(max_length=2, choices=QUARTERS, null=True)
    is_active = models.BooleanField(default=False)
    allocated_budget = models.DecimalField(max_digits=10, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return f'{self.employee.username} - {self.project.name} - {self.quarter} - {self.allocated_budget}'

    @property
    def remaining_budget(self):
        return self.allocated_budget - self.spent_amount if self.allocated_budget else 0

    @property
    def percentage_left(self):
        return (self.remaining_budget / self.allocated_budget) * 100 if self.allocated_budget else 0

class FundRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    requester = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='fund_requests')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    quarter = models.CharField(max_length=2, choices=ProjectEmployeeAllocatedBudget.QUARTERS)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    justification = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    reviewer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='fund_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.requester.username} - {self.project.name} - {self.amount_requested} ({self.status})"


def apply_to_budget(self):
    if self.status == 'Approved':
        budget = ProjectEmployeeAllocatedBudget.objects.get(
            project=self.project,
            quarter=self.quarter,
            employee=self.requester,
        )
        budget.allocated_budget = self.amount_requested
        budget.save()

class Meta:
    unique_together = ('employee', 'project', 'quarter')
    # only one budget per quarter per employee per project is active

class ExpenseType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name





class Expense(models.Model):

    team = models.ForeignKey("Team", on_delete=models.PROTECT)# this won't
    # allow team to be deleted bc expenses exist (this won't happen as
    # existingt expenses are part of the team)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    upload = models.ImageField(upload_to='uploads/', default='uploads/default.png')
    type = models.ForeignKey(ExpenseType, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.description} - {self.employee.account_number}'


    @property
    def expense_quarter(self):
        # look at the created date of the expense
        # expense_quarter = 31 may is second quarter expense because it's between 4 and 6 month of year
    #      so for q1 = jan- march, q2 apr - may , q3 will be july - sep, and q4 oct-dec
    #     extract month from the current created date
        print(self.created_date.month)

    # TODO: To complete by the weekend
    # if month:
    #     jan, feb, march
    #     return q1
    #
    # elif:
    #     april, may, june
    #
    #     return q2
    # elif:
    #     july, august, september
    #     return q3
    # else:
    #     return q4
    #
    # return self.created_date.month

    @property
    def remaining_budget(self):
        """Calculate remaining budget for the current employee in the active quarter."""
        allocated_budget_record = ProjectEmployeeAllocatedBudget.objects.filter(
            employee=self.employee, project=self.project, is_active=True
        ).first()

        if allocated_budget_record:
            total_budget = allocated_budget_record.allocated_budget
            total_expenses = Expense.objects.filter(
                employee=self.employee,
                project=self.project,
                created_date__lte=self.created_date
            ).aggregate(total=Sum('initial_amount'))['total'] or 0

            return total_budget - total_expenses

        return 0  # No allocated budget found


class Team(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='teams', on_delete=models.CASCADE)
    # members = models.ManyToManyField(Employee, related_name='teams')
    description = models.TextField(blank=True, null=True)
    # don't allow employee to be deleted if employee is manager of team
    # if you delete employee you must also delete team employee was a part of
    manager = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="managed_team",
        blank = True,null=True,

    )

    def __str__(self):
        return f'{self.name} - {self.project} - {self.description}'


class Receipt(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.description} - {self.amount}'
