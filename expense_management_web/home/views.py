from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from incomes.models import CategoryIncome, Income,BudgetIncome
from expenses.models import CategoryExpense, Expense,BudgetExpense
from django.db.models import Sum
from datetime import datetime
from django.db.models import Q, Max


@login_required(login_url='/login/')
def index(request):
    print(request.POST)
    income_categories = CategoryIncome.objects.filter(user=request.user)
    incomes = Income.objects.filter(category__in=income_categories)

    expense_categories = CategoryExpense.objects.filter(user=request.user)
    expenses = Expense.objects.filter(category__in=expense_categories)

    month = request.POST.get('month')
    print(month) 

    latest_year = datetime.now().year

    current_income = 0
    current_expense = 0
    current_balance = 0
    total_expense = 0
    expense_category_totals = 0

    total_income = 0
    income_category_totals = 0

        # Xử lý khi month là None hoặc rỗng
    incomes = incomes.filter(date__year=latest_year)
    latest_year = Income.objects.filter(category__user=request.user).aggregate(latest_year=Max('date__year'))['latest_year']
    latest_year_income_totals = Income.objects.filter(date__year=latest_year, category__user=request.user).values('category__name').annotate(total_amount=Sum('amount'))
    income_category_totals = latest_year_income_totals.filter(total_amount__gt=0)
    total_income = Income.objects.filter(date__year=latest_year, category__user=request.user).aggregate(total_amount=Sum('amount'))['total_amount']



    latest_year = Expense.objects.filter(category__user=request.user).aggregate(latest_year=Max('date__year'))['latest_year']
    expenses = expenses.filter(date__year=latest_year)
    latest_year_expense_totals = Expense.objects.filter(date__year=latest_year, category__user=request.user).values('category__name').annotate(total_amount=Sum('amount'))
    expense_category_totals = latest_year_expense_totals.filter(total_amount__gt=0)
    total_expense = Expense.objects.filter(date__year=latest_year, category__user=request.user).aggregate(total_amount=Sum('amount'))['total_amount']
   
    if not total_income: 
        total_income = 0
    if not total_expense:
        total_expense = 0
    current_income = total_income 
    current_expense = total_expense 
    current_balance = current_income - current_expense 
    # print(current_balance)
    print(current_income)
    print(current_expense)

    if month:
        if month != '': 
            incomes = incomes.filter(date__month=month)
            income_category_totals = Income.objects.filter(date__month=month, category__user=request.user).values('category__name').annotate(total_amount=Sum('amount'))
            income_category_totals = income_category_totals.filter(total_amount__gt=0)
            total_income = Income.objects.filter(date__month=month, category__user=request.user).aggregate(total_amount=Sum('amount'))['total_amount']

            expenses = expenses.filter(date__month=month)
            expense_category_totals = Expense.objects.filter(date__month=month, category__user=request.user).values('category__name').annotate(total_amount=Sum('amount'))
            expense_category_totals = expense_category_totals.filter(total_amount__gt=0)
            total_expense = Expense.objects.filter(date__month=month, category__user=request.user).aggregate(total_amount=Sum('amount'))['total_amount']



    incomes = incomes[:4]
    expenses = expenses[:4]

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
    print(saving)
    print(total_saving)

    return render(request, 'home/dashboard.html', {'incomes': incomes, 'expenses': expenses,
                            'user': request.user, 'month': month,
                            'expense_category_totals': expense_category_totals, 'total_expense': total_expense,
                            'income_category_totals': income_category_totals, 'total_income': total_income,
                            'current_balance': current_balance, 'current_income': current_income, 'current_expense': current_expense, 'total_saving': total_saving})
