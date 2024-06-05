from django.shortcuts import render, redirect
from .forms import registerForm, loginForm
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.http import HttpResponse

from incomes.models import CategoryIncome, Income, BudgetIncome
from expenses.models import CategoryExpense, Expense, BudgetExpense

def index(request):
    return render(request, 'users/home.html')
# Create your views here.
class registerUser(View):
    def get(self, request):
        # rF = registerForm()
        return render(request, 'users/register.html')
 
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', { 'error': 'Username already exists'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'users/register.html', { 'error': 'Email already exists'})
        elif password != repassword:
            return render(request, 'users/register.html', { 'error': 'Passwords do not match',  'username': username, 'email': email})
        else:
            user = User.objects.create_user(username, email, password)
            categoryIncome = CategoryIncome.objects.create(user=user, name='Nothing')
            categoryIncome.save()
            categoryExpense = CategoryExpense.objects.create(user=user, name='Nothing')
            categoryExpense.save()
            user.save()
            return redirect('users:loginUser')
        
class loginUser(View):
    def get(self, request):
        # lF = loginForm()
        return render(request, 'users/login.html')
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username is an email
        if '@' in username:
            if User.objects.filter(email=username).exists():
                # If the email exists, try to authenticate the user
                user = authenticate(request, username=User.objects.get(email=username).username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home:home')
                else:
                    return render(request, 'users/login.html', { 'error': 'Incorrect password. Please try again.'})
            else:
                return render(request, 'users/login.html', { 'error': 'Email does not exist, please create a new account'})
        else:
            # If the username is not an email, try to authenticate the user
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home:home')
                else:
                    return render(request, 'users/login.html', { 'error': 'Incorrect password. Please try again.', 'username': username})
            else:
                return render(request, 'users/login.html', { 'error': 'Username is incorrect. Please try again.'})



def logoutUser(request):
    logout(request)
    # redirect đến url
    return redirect('users:index')
    # return HttpResponse('Logged out successfully')




def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'exists': User.objects.filter(username=username).exists()
    }
    return JsonResponse(data)

def check_email(request):
    email = request.GET.get('email', None)
    data = {
        'exists': User.objects.filter(email=email).exists()
    }
    return JsonResponse(data)