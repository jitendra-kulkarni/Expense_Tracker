from urllib import request
from django.shortcuts import render, redirect
from .models import Expense, Budget
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum
from datetime import date
from datetime import datetime
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from django.contrib.messages import get_messages
from django.db.models.functions import TruncMonth
from datetime import timedelta
import json
import calendar
from django.core.paginator import Paginator

today = date.today()

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
    
    expenses_list = Expense.objects.filter(
        user=request.user,
    ).order_by('-date')

    search = request.GET.get("search")

    if search:
        expenses_list=expenses.filter(
            title__icontains = search
        )

    month=request.GET.get("month")
    year=request.GET.get("year")

    if month and year:
        expenses_list = expenses_list.filter(
            date__month = month,
            date__year = year
        )

    paginator = Paginator(expenses_list, 5)

    page_number = request.GET.get('page')

    expenses = paginator.get_page(page_number)
    
    this_month_expenses = Expense.objects.filter(
        user=request.user,
        date__month = today.month,
        date__year = today.year
    )

    current_month = datetime.now().month
    current_year = datetime.now().year

    budget = Budget.objects.filter(
        user=request.user,
        month = current_month,
        year = current_year
    ).first()

    this_month_total = this_month_expenses.aggregate(
        Sum("amount")
    )["amount__sum"] or 0


    budget_amount = budget.amount if budget else 0

    remaining_budget = budget_amount - this_month_total

    if budget_amount > 0:
        spent_percentage = (this_month_total / budget_amount) * 100

        if spent_percentage > 100:
            spent_percentage = 100

    else:
         spent_percentage = 0

    total_transactions = expenses_list.count()

    total_expense = expenses_list.aggregate(
        Sum("amount")

    )["amount__sum"] or 0

    chart_labels = []
    chart_data = []

    current_date = timezone.now()

    for i in range(5, -1, -1):
        month = current_date.month - i
        year = current_date.year

        while month <= 0:
            month += 12
            year -= 1

        total = Expense.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year
        ).aggregate(Sum("amount"))["amount__sum"] or 0

        chart_labels.append(calendar.month_abbr[month])

        chart_data.append(float(total))

    context = {
        "Expenses":expenses,
        "total_transaction":total_transactions,
        "total_expense":total_expense,
        "this_month_total":this_month_total,
        'budget_amount':budget_amount,
        'remaining_budget': remaining_budget,
        'spent_percentage': spent_percentage,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),

    }

    return render(request, "home.html",context) 


def register_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login_page")
    
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

            storage = get_messages(request)
            for _ in storage:
                pass

            messages.success(request, f"Welcome back, {request.user.username}")
            return redirect('home')
        
        else:
            messages.error(request, "Invalid Username or Password !!!")

    return render(request, 'login_page.html')


def logout_page(request):

    logout(request)

    return redirect('login_page')


@login_required(login_url='login_page')
def delete_expense(request, id):
    expense = Expense.objects.get(id=id,
        user=request.user
    )
    expense.delete()
    return redirect('home')


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

        return redirect('home')
    
    return render(request, 'edit_expense.html',{
        'expense':expense
    })

@login_required(login_url='/login/')
def update_budget(request):
    current_month = timezone.now().month
    current_year = timezone.now().year

    budget = Budget.objects.filter(
        user=request.user,
        month=current_month,
        year=current_year
    ).first()

    if request.method == 'POST':

        amount = request.POST.get('amount')
        if budget:

            budget.amount = amount
            budget.save()

        else:
            Budget.objects.create(
                user=request.user,
                amount=amount,
                month=current_month,
                year=current_year
            )

        return redirect('/')
    
    return render(request, 'budget.html',{
        "budget":budget
    })


