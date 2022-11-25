from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from django.core.paginator import Paginator


def payment_list(request):
    """View function that return the page with user payment list"""
    payment_list = Payment.objects.all().order_by('-due_date').filter(provider=request.user)
    
    paginator = Paginator(payment_list, 3)

    page = request.GET.get('page')

    payments = paginator.get_page(page)

    return render(request, 'payments/payments.html', {'payments': payments})


def payment_view(request, id):
    """
    View Funcition that return payment info"""
    #payment = get_object_or_404(Payment, pk=id, provider=request.user)
    payment = get_object_or_404(Payment, pk=id)
    return render(request, 'payments/payment_view.html', {'payment': payment})






