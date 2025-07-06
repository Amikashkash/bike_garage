from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CustomerForm
from .forms import BikeForm
from .forms import RepairJobForm
from django.shortcuts import render, redirect
from .permissions import role_required
from .permissions import staff_required, mechanic_required, manager_required
from .models import RepairCategory
from .forms import RepairCategoryForm, RepairSubCategoryForm
from .forms import RepairJobForm
from .models import RepairCategory



@login_required
@role_required(['mechanic', 'manager'])
def repair_form(request):
    if request.method == 'POST':
        form = RepairJobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RepairJobForm()
        categories = RepairCategory.objects.prefetch_related('subcategories').all()
    return render(request, 'workshop/repair_form.html', {
        'form': form,
        'categories': categories,
    })


@login_required
def bike_form(request):
    if request.method == 'POST':
        form = BikeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BikeForm()
    return render(request, 'workshop/bike_form.html', {'form': form})


@login_required
def customer_form(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # נחזיר לדף הבית אחרי שמירה
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

@login_required
@staff_required
def home(request):
    return render(request, "workshop/home.html")

def user_logout(request):
    logout(request)
    return redirect("login")

@staff_required
def category_list(request):
    cats = RepairCategory.objects.prefetch_related('subcategories').all()
    return render(request, 'workshop/repair_form.html', {
    'form': form,
    'categories': categories
})




@staff_required
def category_create(request):
    if request.method == 'POST':
        form = RepairCategoryForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('category_list')
    else:
        form = RepairSubCategoryForm()
    return render(request, 'workshop/subcategory_form.html', {'form': form})
