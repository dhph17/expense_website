from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import CategoryExpense, Expense,BudgetExpense
from .models import get_current_month_expenses, get_monthly_expenses
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Sum
import csv
import io
import codecs
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from django.contrib.staticfiles import finders
# from django.urls import reverse
from django.utils.decorators import method_decorator




@login_required(login_url='/login/')
def index(request):
    categories = CategoryExpense.objects.filter(user=request.user)
    expenses = Expense.objects.filter(category__in=categories)
    categories = CategoryExpense.objects.filter(user=request.user).exclude(name='Nothing')

    date = request.POST.get('datepickerFilter')
    print(date)
    if date:
        expenses = expenses.filter(date=date)

    print(expenses)

    category_name = request.POST.get('category-filter')
    print(category_name)
    if category_name and category_name != 'All':
        expenses = expenses.filter(category__name=category_name)
    # print(categories)
    default_categories = ["Food and drink", "Grocery", "Transportation", "Entertainment", "Education", "Medicine"]

    return render(request, 'expenses/expense.html', {'expenses': expenses, 'user': request.user,'categories': categories, 'default_categories': default_categories})

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class addExpense(View):
    def get(self, request):
        categories = CategoryExpense.objects.filter(user=request.user)
        # return render(request, 'expenses/addExpense.html', {'categories': categories})

    def post(self, request):
        category_name = request.POST.get('your-category')
        amount = request.POST.get('amount')
        note = request.POST.get('note')
        date = request.POST.get('datepickerInputModal')

        if category_name == "Other":
            # request.session['redirect_to_add_expense'] = True
            name = request.POST.get('add-category')
            print(name)
            if name:
                category, created = CategoryExpense.objects.get_or_create(user=request.user, name=name)
                if created:
                    return JsonResponse({'status': 'success', 'message': 'Category added successfully'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Category already exists'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Name is required'})


        category = CategoryExpense.objects.filter(user=request.user, name=category_name).first()
        if not category:
            category = CategoryExpense.objects.create(user=request.user, name=category_name)

        expense = Expense.objects.create(category=category, amount=amount, note=note, date=date)
        expense.save()
        return JsonResponse({'status': 'success', 'message': 'Expense added successfully'})
    


@login_required(login_url='/login/')
def deleteExpenses(request):
    if request.method == 'POST':
        expenses_to_delete = request.POST.getlist('expenses_to_delete')
        Expense.objects.filter(id__in=expenses_to_delete).delete()
    return redirect('expenses:indexExpenses')

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class editExpense(View):
    def get(self, request, expense_id):
        # if request.is_ajax():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            expense = get_object_or_404(Expense, id=expense_id)
            data = {
                'id': expense.id,
                'category': expense.category.name,
                'amount': expense.amount,
                'note': expense.note,
                'date': expense.date.strftime('%Y-%m-%d')
            }
            return JsonResponse(data)
        
    def post(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id)
        category_name = request.POST.get('category')
        amount = request.POST.get('amount')
        note = request.POST.get('note')
        date = request.POST.get('date')

        # print(category_name)
        if category_name == "Other":
            # request.session['redirect_to_add_expense'] = True
            name = request.POST.get('add-category-edit')
            print("edit")
            print(name)
            if name:
                category, created = CategoryExpense.objects.get_or_create(user=request.user, name=name)
                if created:
                    return JsonResponse({'status': 'success', 'message': 'Category added successfully'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Category already exists'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Name is required'})

        category, created = CategoryExpense.objects.get_or_create(user=request.user, name=category_name)

        expense.category = category
        expense.amount = amount
        expense.note = note
        expense.date = date
        expense.save()
        return redirect('expenses:indexExpenses')
    
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class editCategory(View):
    def get(self, request, category_id):
        # if request.is_ajax():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            category_expense = get_object_or_404(CategoryExpense, id=category_id)
            data = {
                'name': category_expense.name
            }
            return JsonResponse(data)
        
    def post(self, request, category_id):
        category = get_object_or_404(CategoryExpense, id=category_id)

        name = request.POST.get('name')

        if CategoryExpense.objects.filter(user=request.user, name=name).exists():
            return JsonResponse({'status': 'error', 'message': 'Category already exists'})
        else:
            category.name = name
            category.save()
            return redirect('expenses:indexExpenses')
        


@login_required(login_url='/login/')
def listCategoryExpense(request):
    categories = CategoryExpense.objects.filter(user=request.user)
    categories_list = list(categories.values('id', 'name'))
    return JsonResponse({'categories': categories_list, 'user': request.user.username})

@csrf_exempt
@login_required(login_url='/login/')
def addCategory(request):
    if request.method == 'POST':
        name = request.POST.get('add-category-modal')
        if name:
            category, created = CategoryExpense.objects.get_or_create(user=request.user, name=name)
            if created:
                return JsonResponse({'status': 'success', 'message': 'Category added successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Category already exists'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Name is required'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class deleteCategory(View):
    def post(self, request):
        category_ids = request.POST.getlist('category_ids')
        print(category_ids)
        for category_id in category_ids:
            category_nothing, created = CategoryExpense.objects.get_or_create(user=request.user, name="Nothing")
            category = CategoryExpense.objects.get(id=category_id)
            expense = Expense.objects.filter(category=category)
            budget = BudgetExpense.objects.filter(category=category)
            # print(expense)
            for i in expense:
                i.category = category_nothing
                i.save()
            
            for i in budget:
                i.category = category_nothing
                i.save()
            
        CategoryExpense.objects.filter(user=request.user, id__in=category_ids).delete()
        
        return JsonResponse({'status': 'success', 'message': 'Category delete successfully'})

# @login_required(login_url='/login/')
def update_total_expense_in_budgets(user):
    categories = CategoryExpense.objects.filter(user=user).exclude(name='Nothing')
    expenses = Expense.objects.filter(category__in=categories)
    budgets = BudgetExpense.objects.filter(category__in=categories)
    
    for budget in budgets:
        total_expense = 0
        budget_expenses = expenses.filter(date__gte=budget.start_date, date__lte=budget.end_date, category=budget.category)
        
        budget_expense_sum = budget_expenses.aggregate(total=Sum('amount'))['total'] or 0
        total_expense += budget_expense_sum
        print(budget, budget_expenses, budget_expense_sum, total_expense)
        budget.total_expense = budget_expense_sum
        budget.save() 


@login_required(login_url='/login/')
def viewBudgets(request):

    savings_data = []
    budget_expenses = BudgetExpense.objects.filter(category__user=request.user)
    total_saving = 0
    
    for budget_expense in budget_expenses:
        expenses_in_budget_period = Expense.objects.filter(
            category=budget_expense.category,
            date__gte=budget_expense.start_date,
            date__lte=budget_expense.end_date
        )
 
        total_expense_in_budget_period = expenses_in_budget_period.aggregate(Sum('amount'))['amount__sum'] or 0
        saving = budget_expense.amount - total_expense_in_budget_period
        total_saving += saving
    
    
        savings_data.append({
            'budget': budget_expense,
            'saving': saving,
            'total_income': total_expense_in_budget_period
        })
    
    print(savings_data)
    categories = CategoryExpense.objects.filter(user=request.user)
    budgets = BudgetExpense.objects.filter(category__in=categories)
    categories = CategoryExpense.objects.filter(user=request.user).exclude(name='Nothing')

    print(budgets)
    return render(request, 'expenses/expenseBudget.html', {'user': request.user, 'categories': categories, 'budgets': budgets, 'savings': savings_data})

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class addBudget(View):

    def post(self, request):
        category_name = request.POST.get('your-category')
        amount = request.POST.get('amount')
        note = request.POST.get('note')
        start_date = request.POST.get('datepickerInput-start')
        end_date = request.POST.get('datepickerInput-end')

        category = CategoryExpense.objects.filter(user=request.user, name=category_name).first()
        # Kiểm tra xem có budget nào cùng category và end_date >= start_date của budget mới không
        overlapping_budgets = BudgetExpense.objects.filter(category=category, end_date__gte=start_date, category__user=request.user)


        if overlapping_budgets.exists():
            print('error')
            return JsonResponse({'status': 'error', 'message': 'There is an overlapping budget'})

        expense = BudgetExpense.objects.create(category=category, amount=amount, note=note, start_date=start_date, end_date=end_date)
        expense.save()
        return JsonResponse({'status': 'success', 'message': 'Add budget successfully'})

@login_required(login_url='/login/')
def deleteBudgets(request):
    if request.method == 'POST':
        budget_expenses_to_delete = request.POST.getlist('budget_to_delete')
        BudgetExpense.objects.filter(id__in=budget_expenses_to_delete).delete()
    return redirect('expenses:viewBudgets')

# @method_decorator(login_required(login_url='/login/'), name='dispatch')
class editBudget(View):
    def get(self, request, budget_id):
        # if request.is_ajax():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            budget = get_object_or_404(BudgetExpense, id=budget_id)
            data = {
                'id': budget.id,
                'category': budget.category.name,
                'amount': budget.amount,
                'note': budget.note,
                'date_start': budget.start_date.strftime('%Y-%m-%d'),
                'date_end': budget.end_date.strftime('%Y-%m-%d')
            }
            return JsonResponse(data)
        
    def post(self, request, budget_id):
        budget = get_object_or_404(BudgetExpense, id=budget_id)
        category_name = request.POST.get('category')
        amount = request.POST.get('amount')
        note = request.POST.get('note')
        start_date = request.POST.get('date_start')
        end_date = request.POST.get('date_end')

        category = CategoryExpense.objects.filter(user=request.user, name=category_name).first()

        overlapping_budgets = BudgetExpense.objects.filter(
            category=category, 
            end_date__gte=start_date,
            category__user=request.user
        ).exclude(id=budget.id)

        if overlapping_budgets.exists():
            return JsonResponse({'status': 'error', 'message': 'There is an overlapping budget'})

        category, created = CategoryExpense.objects.get_or_create(user=request.user, name=category_name)

        budget.category = category
        budget.amount = amount
        budget.note = note
        budget.start_date = start_date
        budget.end_date = end_date
        budget.save()

        return redirect('expenses:viewBudgets')


@login_required(login_url='/login/')
def export_csv(request):
    print("export")
 
    stream = io.BytesIO()
    writer = csv.writer(codecs.getwriter('utf-8-sig')(stream))
    writer.writerow(['Category', 'Amount', 'Note', 'Date'])
 
    # categories = CategoryExpense.objects.filter(user=request.user)
    # expenses = Expense.objects.filter(category__in=categories)
 
    expenses = Expense.objects.filter(category__user=request.user)
    for expense in expenses:
        writer.writerow([expense.category.name, expense.amount, expense.note, expense.date])
 
    response = HttpResponse(stream.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Expenses.csv"'
 
    return response
 
 
 
@login_required(login_url='/login/')
def export_pdf(request):
    # Tìm đường dẫn tuyệt đối đến file font chữ trong thư mục static
    font_path = finders.find('fonts/Roboto-Regular.ttf')
    bold_font_path = finders.find('fonts/Roboto-Bold.ttf')
 
    # Đăng ký font chữ tùy chỉnh
    pdfmetrics.registerFont(TTFont('Roboto', font_path))
    pdfmetrics.registerFont(TTFont('Roboto-Bold', bold_font_path))
 
    # Tạo một bộ đệm byte stream
    buffer = io.BytesIO()
 
    # Tạo canvas
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
 
    # Đặt tiêu đề
    title = "Expenses Report"
    p.setFont("Roboto-Bold", 16)
    p.drawCentredString(width / 2.0, height - 1 * inch, title)
 
    # Draw a line separator below the title
    p.line(0.5 * inch, height - 1.1 * inch, width - 0.5 * inch, height - 1.1 * inch)
 
    # Column headers
    p.setFont("Roboto-Bold", 12)
    p.drawString(1 * inch, height - 1.5 * inch, "Category")
    p.drawString(3 * inch, height - 1.5 * inch, "Amount")
    p.drawString(5 * inch, height - 1.5 * inch, "Note")
    p.drawString(7 * inch, height - 1.5 * inch, "Date")
 
  # Draw a line separator below the headers
    p.line(0.5 * inch, height - 1.6 * inch, width - 0.5 * inch, height - 1.6 * inch)
 
    # Fetch data from the database
    expenses = Expense.objects.filter(category__user=request.user)
 
    # Set initial y position
    y = height - 2 * inch
    p.setFont("Roboto", 12)
 
    for expense in expenses:
        p.drawString(1 * inch, y, expense.category.name)
        p.drawString(3 * inch, y, str(expense.amount))
        p.drawString(5 * inch, y, expense.note)
        p.drawString(7 * inch, y, expense.date.strftime("%Y-%m-%d"))
        y -= 0.5 * inch
 
 
        # If the y position is too low, create a new page
        if y < 1 * inch:
            p.showPage()
            y = height - 1 * inch
            p.setFont("Roboto", 12)
 
    # Save the PDF
    p.showPage()
    p.save()
    # Lấy giá trị của buffer và viết nó vào response
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Expenses.pdf"'
 
    return response