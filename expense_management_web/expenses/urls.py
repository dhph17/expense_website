
from django.urls import path
from . import views
app_name = 'expenses'
urlpatterns = [

    path('index/', views.index, name='indexExpenses'),
    path('deleteExpenses/', views.deleteExpenses, name='deleteExpenses'),
    
    path('addCategoryExpense/', views.addCategory, name='addCategory'), 
    path('editCategoryExpenses/<int:category_id>/', views.editCategory.as_view(), name='editCategory'),

    path('addExpense/', views.addExpense.as_view(), name='addExpense'),
    path('editExpense/<int:expense_id>/', views.editExpense.as_view(), name='editExpense'),
    path('deleteCategoryExpenses/', views.deleteCategory.as_view(), name='deleteCategory'),



    path('viewBudgets/', views.viewBudgets, name='viewBudgets'),
    path('addBudgetExpenses/', views.addBudget.as_view(), name='addBudget'),
    path('deleteBudgetExpenses/', views.deleteBudgets, name='deleteBudgets'),
    path('editBudgetExpenses/<int:budget_id>/', views.editBudget.as_view(), name='editBudget'),

    path('exportExpenses/', views.export_csv, name='exportExpenses'),
    path('exportpdfExpenses/', views.export_pdf, name='export_pdfExpenses'),

]

