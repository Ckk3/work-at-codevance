from django.shortcuts import render, redirect
from .models import Payment
from django.core.paginator import Paginator


def payment_list(request):
    payment_list = Payment.objects.all().order_by('-due_date')
    #payment_list = Payment.objects.all().order_by('-due_date').filter(user=request.user)

    #tasks_done_recently = Task.objects.filter(done='2', user=request.user,updated_at__gt=datetime.datetime.now()-datetime.timedelta(days=30)).count()
    #tasks_done = Task.objects.filter(done='2', user=request.user).count()
    #tasks_doing = Task.objects.filter(done='1', user=request.user).count()
    
    paginator = Paginator(payment_list, 3)

    page = request.GET.get('page')

    payments = paginator.get_page(page)

    return render(request, 'payments/payments.html', {'payments': payments})
