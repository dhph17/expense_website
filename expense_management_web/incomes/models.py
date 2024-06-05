
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class CategoryIncome(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_category_incomes')
    name = models.CharField(max_length=255)  # Ensure unique category names

    def __str__(self):
        return f"{self.name}"
    class Meta:
        unique_together = ('user', 'name')


class Income(models.Model):
    # owner = models.ForeignKey(to=User, related_name='Incomes', on_delete=models.CASCADE)
    amount = models.IntegerField()
    note = models.TextField(blank=True)
    category = models.ForeignKey(to=CategoryIncome, on_delete=models.CASCADE, related_name='category_incomes')
    date = models.DateField(default=now)

    def __str__(self):
        return f" {self.category} - {self.amount} - {self.date} - {self.note}"  # More informative string representation

    class Meta:
        ordering = ['-date']

class BudgetIncome(models.Model):
    # user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_budgets')
    category = models.ForeignKey(to=CategoryIncome, on_delete=models.CASCADE, related_name='category_budget_incomes')
    amount = models.IntegerField()
    note = models.TextField(blank=True)
    start_date = models.DateField(default=now)
    end_date = models.DateField()
    total_income = 0

    def __str__(self):
        return f"{self.category} - {self.amount} - {self.note} - {self.start_date} - {self.end_date} - {self.total_income}"  # More informative string representation

    class Meta:
        unique_together = ( 'category', 'start_date', 'end_date')  # Enforce unique budget per user, category, start date, and end date
