
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime


# Create your models here.
class CategoryExpense(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_category_expenses')
    name = models.CharField(max_length=255)  # Ensure unique category names

    def __str__(self):
        return f" {self.name}"
    class Meta:
        unique_together = ('user', 'name')
        ordering = ['-id']


class Expense(models.Model):
    # owner = models.ForeignKey(to=User, related_name='Expenses', on_delete=models.CASCADE)
    amount = models.IntegerField()
    note = models.TextField(blank=True)
    category = models.ForeignKey(to=CategoryExpense, on_delete=models.CASCADE, related_name='category_expenses')
    date = models.DateField(default=now)

    def __str__(self):
        return f" {self.category} - {self.amount} - {self.date} - {self.note}"  # More informative string representation

    class Meta:
        ordering = ['-date']

class BudgetExpense(models.Model):
    # user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_budgets')
    category = models.ForeignKey(to=CategoryExpense, on_delete=models.CASCADE, related_name='category_budgets')
    amount = models.IntegerField()
    note = models.TextField(blank=True)
    start_date = models.DateField(default=now)
    end_date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount} - {self.note} - {self.start_date} - {self.end_date}"  # More informative string representation

    class Meta:
        ordering = ['-start_date']
        unique_together = ('category', 'start_date', 'end_date')  # Enforce unique budget per user, category, start date, and end date


def get_monthly_expenses(user):
    return Expense.objects.filter(category__user=user).annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).values('month', 'total_amount')



def get_current_month_expenses(user):
    current_month = datetime.now().month
    current_year = datetime.now().year
    expenses = Expense.objects.filter(category__user=user, date__year=current_year, date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).values('month', 'total_amount')
    return expenses[0] if expenses else None