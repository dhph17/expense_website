
from django.urls import path
from . import views
app_name = 'incomes'
urlpatterns = [
    # path('', views.test, name='test'),
    path('index/', views.index, name='indexIncomes'),
    path('addIncome/', views.addIncome.as_view(), name='addIncome'),
    path('deleteIncomes/', views.deleteIncomes, name='deleteIncomes'),
    path('editIncome/<int:income_id>/', views.editIncome.as_view(), name='editIncome'),

    path('addCategoryIncomes/', views.addCategory.as_view(), name='addCategory'), 
    path('editCategoryIncomes/<int:category_id>/', views.editCategory.as_view(), name='editCategory'),
    path('deleteCategoryIncomes/', views.deleteCategory.as_view(), name='deleteCategory'),

    path('viewBudgets/', views.viewBudgets, name='viewBudgets'),
    path('addBudgetIncomes/', views.addBudget.as_view(), name='addBudget'),
    path('deleteBudgetIncomes/', views.deleteBudgets, name='deleteBudgets'),
    path('editBudgetIncomes/<int:budget_id>/', views.editBudget.as_view(), name='editBudget'),

    path('exportIncomes/', views.export_csv, name='exportIncomes'),
    path('exportpdfIncomes/', views.export_pdf, name='export_pdfIncomes'),


]
