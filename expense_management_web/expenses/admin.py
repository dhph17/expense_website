from django.contrib import admin
from .models import CategoryExpense, Expense, BudgetExpense

# admin.site.register(CategoryExpense)
# admin.site.register(Expense)
# admin.site.register(BudgetExpense)

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
  list_display = ("user", "name")
  
admin.site.register(CategoryExpense, CategoryAdmin)

class ExpenseAdmin(admin.ModelAdmin):
  list_display = ("category", "amount", "note","date")
admin.site.register(Expense, ExpenseAdmin)

class BudgetAdmin(admin.ModelAdmin):
  list_display = ("category", "amount", "note","start_date", "end_date")
admin.site.register(BudgetExpense, BudgetAdmin)