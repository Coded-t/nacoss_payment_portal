from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User, Payment
import random
import string

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        email = request.POST['email']
        matric_number = request.POST['matric_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        if User.objects.filter(matric_number=matric_number).exists():
            messages.error(request, 'Matric number already exists')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'register.html')

        user = User.objects.create_user(
            matric_number=matric_number,
            email=email,
            password=password,
            first_name=first_name
        )
        messages.success(request, 'Registration successful')
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        matric_number = request.POST['matric_number']
        password = request.POST['password']
        user = authenticate(request, matric_number=matric_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid matric number or password')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def dues(request):
    # Define available fees
    fees = [
        {'name': 'Practical Manual', 'amount': 2000.00},
        {'name': 'Handout', 'amount': 1500.00},
        {'name': 'Vest', 'amount': 3000.00},
        {'name': 'Project Fees', 'amount': 2500.00},
    ]
    return render(request, 'dues.html', {'fees': fees})

@login_required
def payment_method(request):
    amount = request.GET.get('amount')
    fee_name = request.GET.get('fee')
    if not amount or not fee_name:
        return redirect('dues')
    if request.method == 'POST':
        method = request.POST.get('method')
        amount = request.POST.get('amount')
        fee_name = request.POST.get('fee_name')
        if not method or not amount or not fee_name:
            messages.error(request, 'Please select a payment method and ensure amount is provided.')
            return redirect('payment_method')
        reference_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        payment = Payment.objects.create(
            user=request.user,
            amount=amount,
            reference_number=reference_number,
            payment_method=method
        )

        if method == 'card':
            messages.info(request, 'Card payment method will be added soon.')
            return redirect('dashboard')
        elif method == 'bank_transfer':
            return render(request, 'bank_transfer.html', {'payment': payment, 'fee_name': fee_name})
    return render(request, 'payment_method.html', {'amount': amount, 'fee_name': fee_name})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
