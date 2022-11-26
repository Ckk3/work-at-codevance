from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment, Anticipate
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import datetime
from decimal import Decimal
from braces.views import GroupRequiredMixin


@login_required
def redirect_view(request):
    """This view search for user group and redirect to payments (if fornecedor) or anticipates (if operador or admin)
    """
    # get all user groups
    if check_group(request=request, group='fornecedores'):
        return redirect('/payments')
    elif check_group(request=request, group='operadores'):
        return redirect('/anticipates')
    

@login_required
def payment_list(request):
    """View that shows payment to every user"""
    payment_list = Payment.objects.all().order_by('-due_date', 'paid').filter(provider=request.user)
    
    paginator = Paginator(payment_list, 3)

    page = request.GET.get('page')

    payments = paginator.get_page(page)

    return render(request, 'payments/payments.html', {'payments': payments})

@login_required
def payment_view(request, id):
    """
    View Funcition that return payment info"""
    payment = get_object_or_404(Payment, pk=id, provider=request.user) 

    original_value, new_value, original_due_date, new_due_date, days_delta = get_antecipate_value(payment=payment)
    return render(request, 'payments/payment_view.html', {'payment': payment, 'original_value': original_value, 'new_value': new_value, 'original_due_date': original_due_date, 'new_due_date': new_due_date, 'days_delta':days_delta})

@login_required
def anticipate_request_view(request, id):
    """Request anticipate payment"""
    #get payment
    payment = get_object_or_404(Payment, pk=id, provider=request.user)
    # Get antecipate informations
    original_value, new_value, original_due_date, new_due_date, days_delta = get_antecipate_value(payment=payment)

    new_anticipate = Anticipate(
        old_due_date = original_due_date,
        new_due_date = new_due_date,
        payment = payment,
        original_value = original_value,
        new_value = new_value,
    )

    # Add new anticipate
    new_anticipate.save()
    # Change payment status to requested
    payment.status = 'requested'
    payment.save()

    #messages.info(request, 'Anticipate request done')
    #Return to home
    return redirect('/')


@login_required
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


def check_group(request, group):
    """
    Check if user is in the group.

    Return False if user is not in the group
    """
    user_groups = list(request.user.groups.values_list('name', flat = True))
    
    return group in user_groups









