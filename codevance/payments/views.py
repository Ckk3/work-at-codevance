from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from django.core.paginator import Paginator
import datetime
from decimal import Decimal


def payment_list(request):
    """View function that return the page with user payment list"""
    #payment_list = Payment.objects.all().order_by('-due_date').filter(provider=request.user)
    payment_list = Payment.objects.all().order_by('-due_date', 'paid')
    
    paginator = Paginator(payment_list, 3)

    page = request.GET.get('page')

    payments = paginator.get_page(page)

    return render(request, 'payments/payments.html', {'payments': payments})


def payment_view(request, id):
    """
    View Funcition that return payment info"""
    #payment = get_object_or_404(Payment, pk=id, provider=request.user)
    #get payment and require
    payment = get_object_or_404(Payment, pk=id) 
    return render(request, 'payments/payment_view.html', {'payment': payment})

def anticipate_request_view(request, id):
    pass

def anticipate_info_view(request, id):
    """Calculate antecipated info about a payment"""
    payment = get_object_or_404(Payment, pk=id)

    if payment.paid == False:
        original_value, new_value, original_due_date, new_due_date, days_delta = get_antecipate_value(payment=payment)
        return render(request, 'payments/antecipate_payment_view.html', {'payment': payment, 'original_value': original_value, 'new_value': new_value, 'original_due_date': original_due_date, 'new_due_date': new_due_date, 'days_delta':days_delta})


def get_antecipate_value(payment):
    """
    Calculate antecipated new value using payment object using this calculum
    NEW_VALUE = ORIGINAL_VALUE - (ORIGINAL_VALUE * ((3% / 30) * DAYS_DELTA))
    
    """
    original_value = payment.original_value
    original_due_date = payment.due_date
    new_due_date = datetime.date.today()

    # Calculate days difference using timedelta object
    days_delta = original_due_date - datetime.date.today()
    days_delta = days_delta.days

    # Calcute new value using
    new_value = round(Decimal(original_value - (original_value * Decimal(((3/100) / 30) * days_delta))), ndigits=2)

    return original_value, new_value, original_due_date, new_due_date, days_delta










