from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .forms import (
    CustomerForm, BikeForm, RepairJobForm, RepairCategoryForm, 
    RepairSubCategoryForm, CustomerRegisterForm, CustomerRepairJobForm
)
from .models import Customer, Bike, RepairCategory, RepairJob
from .permissions import role_required, staff_required, mechanic_required, manager_required




@login_required
def customer_report(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, "לא נמצא פרופיל לקוח עבור המשתמש הזה")
        return redirect('home')
    
    bikes = Bike.objects.filter(customer=customer)
    if request.method == 'POST':
        form = CustomerRepairJobForm(request.POST)
        form.fields['bike'].queryset = bikes
        if form.is_valid():
            repair = form.save(commit=False)
            if repair.bike in bikes:
                repair.save()
                form.save_m2m()
                messages.success(request, "הדיווח נשלח בהצלחה!")
                return render(request, 'workshop/customer_report_done.html')
    else:
        form = CustomerRepairJobForm()
        form.fields['bike'].queryset = bikes
    return render(request, 'workshop/customer_report.html', {'form': form})


@login_required
@role_required(['mechanic', 'manager'])
def repair_form(request):
    if request.method == 'POST':
        form = RepairJobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "התיקון נוצר בהצלחה!")
            return redirect('home')
    else:
        form = RepairJobForm()
    categories = RepairCategory.objects.prefetch_related('subcategories').all()
    return render(request, 'workshop/repair_form.html', {
        'form': form,
        'categories': categories,
    })


@login_required
@staff_required
def bike_form(request):
    if request.method == 'POST':
        form = BikeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "האופניים נוספו בהצלחה!")
            return redirect('home')
    else:
        form = BikeForm()
    return render(request, 'workshop/bike_form.html', {'form': form})


@login_required
@staff_required
def customer_form(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "הלקוח נוצר בהצלחה!")
            return redirect('home')
    else:
        form = CustomerForm()
    return render(request, 'workshop/customer_form.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'workshop/login.html', {'error': 'שם משתמש או סיסמה שגויים'})
    return render(request, 'workshop/login.html')


def home(request):
    return render(request, "workshop/home.html")

def user_logout(request):
    logout(request)
    return redirect("login")

@staff_required
def category_list(request):
    categories = RepairCategory.objects.prefetch_related('subcategories').all()
    return render(request, 'workshop/category_list.html', {'categories': categories})




@staff_required
def category_create(request):
    if request.method == 'POST':
        form = RepairCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "הקטגוריה נוצרה בהצלחה!")
            return redirect('category_list')
    else:
        form = RepairCategoryForm()
    return render(request, 'workshop/category_form.html', {'form': form})

@staff_required
def subcategory_create(request):
    if request.method == 'POST':
        form = RepairSubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "תת-הקטגוריה נוצרה בהצלחה!")
            return redirect('category_list')
    else:
        form = RepairSubCategoryForm()
    return render(request, 'workshop/subcategory_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "נרשמת בהצלחה!")
            return redirect('home')
    else:
        form = CustomerRegisterForm()
    return render(request, 'workshop/register.html', {'form': form})


