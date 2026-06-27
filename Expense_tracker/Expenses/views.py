from django.shortcuts import render, redirect
from .models import Expense
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    if request.method == "POST":

        title = request.POST.get("title")
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        date = request.POST.get("date")

        Expense.objects.create(
            user = request.user,
            title = title,
            amount = amount,
            category = category,
            date = date 
        )
        
        return redirect('/')
    
    expenses = Expense.objects.filter(
        user=request.user
    )

    total_transactions = expenses.count()

    total_expense = expenses.aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    context = {
        "Expenses":expenses,
        "total_transaction":total_transactions,
        "total_expense":total_expense,
    }

    return render(request, "home.html",context) 


def register_page(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/')
    
    return render(request, 'register.html')


def login_page(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,
            username=username,
            password=password 
        )

        if user is not None:
            login(request, user)
            return redirect('/')
        
        else:
            messages.error(request, "Invalid Username or Password !!!")

    return render(request, 'login_page.html')


def logout_page(request):

    logout(request)

    return redirect('/login/')

def delete_expense(request, id):
    expense = Expense.objects.get(id=id,
        user=request.user
    )
    expense.delete()
    return redirect('/')


def edit_expense(request, id):
    expense = Expense.objects.get(id=id, 
        user=request.user
    )
    if request.method == 'POST':
        expense.title = request.POST.get('title')
        expense.amount = request.POST.get('amount')
        expense.category = request.POST.get('category')
        expense.date = request.POST.get('date')

        expense.save()

        return redirect('/')
    
    return render(request, 'edit_expense.html',{
        'expense':expense
    })


