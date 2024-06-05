
# from django.contrib import admin
# from .models import CategoryIncome, Income, BudgetIncome

# # Register your models here.
# admin.site.register(CategoryIncome)
# admin.site.register(Income)
# admin.site.register(BudgetIncome)

from django.contrib import admin
from .models import CategoryIncome, Income, BudgetIncome

# admin.site.register(CategoryIncome)
# admin.site.register(Income)
# admin.site.register(BudgetIncome)

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
  list_display = ("user", "name")
  
admin.site.register(CategoryIncome, CategoryAdmin)

class IncomeAdmin(admin.ModelAdmin):
  list_display = ("category", "amount", "note","date")
admin.site.register(Income, IncomeAdmin)

class BudgetAdmin(admin.ModelAdmin):
  list_display = ("category", "amount", "note","start_date", "end_date")
admin.site.register(BudgetIncome, BudgetAdmin)