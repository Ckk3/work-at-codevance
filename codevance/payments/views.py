from django.shortcuts import render, redirect
from .models import Payment
from django.core.paginator import Paginator


def payment_list(request):
    payment_list = Payment.objects.all().order_by('-due_date').filter(provider=request.user)
    
    paginator = Paginator(payment_list, 3)

    page = request.GET.get('page')

    payments = paginator.get_page(page)

    return render(request, 'payments/payments.html', {'payments': payments})
