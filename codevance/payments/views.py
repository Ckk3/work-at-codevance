from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment, Anticipate
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import datetime
from decimal import Decimal
from .forms import PaymentForm
from django.contrib import messages
from django.shortcuts import HttpResponse
import logging
from .tasks import send_email_task

#Create logger
logger = logging.getLogger('payment')



def send_email(request, payment, subject):
    """Send email using celery
    subject is the type of the email: request, accepted or denied"""
    all_subjects = {
        'request': 'We receive your anticipate request.',
        'accepted': 'Your anticipate request has been ACCEPTED',
        'denied': 'Your anticipate request has been DENIED'
    }

    all_messages = {
        'request': f'The anticipate request to payment {payment.id} with due date to {payment.due_date} has been added and you will receive a awnser soon!',
        'accepted': f'The anticipate request to payment {payment.id} has been ACCEPTED!\nThe new due date is {payment.due_date} and the new value is R${payment.value}',
        'denied': f'The anticipate request to payment {payment.id} has been DENIED!\nThe due date still {payment.due_date} and the value is R${payment.value}'
    }


    send_email_task.delay(user_email=payment.provider.email, email_subject=all_subjects[subject], email_message=all_messages[subject])
    logger.info(f'Send email to "funcionario" {request.user.id}')
    return None

@login_required
def redirect_view(request):
    """This view search for user group and redirect to payments (if fornecedor) or anticipates (if operador or admin)
    """
    # get all user groups
    if check_group(request=request, group='fornecedores'):
        logger.info('"fornecedor" redirect to /payments')
        return redirect('/payments')
    elif check_group(request=request, group='operadores'):
        logger.info('"operador" redirect to /anticipates')
        return redirect('/anticipates')
    else:
        return render_not_allowed(request)
    

@login_required
def payment_list(request):
    """View that shows payment to every user"""

    #Check if user has permission to see this page
    if not check_group(request=request, group='fornecedores'):
        return render_not_allowed(request)


    payment_list = Payment.objects.all().order_by('-due_date', 'paid').filter(provider=request.user)
    

    paginator = Paginator(payment_list, 3)

    page = request.GET.get('page')

    payments = paginator.get_page(page)

    logger.info(f'List all payments from user {request.user.id}')
    return render(request, 'payments/payments.html', {'payments': payments})


@login_required
def anticipate_list(request):
    """View that shows anticipate to every operator"""

    #Check if user has permission to see this page
    if not check_group(request=request, group='operadores'):
        return render_not_allowed(request)

    anticipate_list = Anticipate.objects.all().order_by('-new_due_date', 'status')
    
    paginator = Paginator(anticipate_list, 3)

    page = request.GET.get('page')

    anticipates = paginator.get_page(page)

    logger.info(f'List all anticipates to operador with id {request.user.id}')
    return render(request, 'payments/anticipates.html', {'anticipates': anticipates})



@login_required
def payment_view(request, id):
    """
    View Funcition that return payment info"""

    #Check if user has permission to see this page
    if not check_group(request=request, group='fornecedores'):
        return render_not_allowed(request)

    #get payment by id or return 404
    payment = get_object_or_404(Payment, pk=id, provider=request.user) 

    logger.info(f'Show payment {payment.id} info')
    #Verify if can anticipate the payment
    can_anticipate = check_can_anticipate(payment=payment)

    original_value, new_value, original_due_date, new_due_date, days_delta = get_antecipate_value(payment=payment)

    return render(request, 'payments/payment_view.html', {'payment': payment, 'original_value': original_value, 'new_value': new_value, 'original_due_date': original_due_date, 'new_due_date': new_due_date, 'days_delta':days_delta, 'can_anticipate':can_anticipate})

@login_required
def anticipate_view(request, id):
    """
    View Funcition that return payment info"""

    #Check if user has permission to see this page
    if not check_group(request=request, group='operadores'):
        return render_not_allowed(request)
    
    #get payment by id or return 404
    anticipate = get_object_or_404(Anticipate, pk=id) 
    payment = get_object_or_404(Payment, pk=anticipate.payment_id)

    logger.info(f'Show anticipate {anticipate.id} info')

    return render(request, 'payments/anticipate_view.html', {'anticipate': anticipate, 'payment':payment})

@login_required
def new_payment(request):
    """View to add a new payment"""
    if not check_group(request=request, group='fornecedores'):
        return render_not_allowed(request)

    #Check if is a POST to a new payment
    if request.method == 'POST':
        # Verify if form is valid
        logger.info(f'Receiving POST of new payment')
        form = PaymentForm(request.POST)

        if form.is_valid():
            #Create payment but not save, still data to add
            new_payment = form.save(commit=False)
            # Add missing data
            new_payment.provider = request.user
            new_payment.old_due_date = new_payment.due_date
            new_payment.original_value = new_payment.value
            new_payment.save()
            logger.info(f'Saved new payment {new_payment.id} to database')
            #Return to home
            return redirect('/payments')
    
    else:
        logger.info(f'Show form to create a new payment')
        form = PaymentForm()
        return render(request, 'payments/add_payment.html', {'form': form})

@login_required
def edit_anticipate_status(request, id, new_status):
    """View to change anticipate status"""

    #Check if user has permission to see this page
    if not check_group(request=request, group='operadores'):
        return render_not_allowed(request)

    # Get anticipate object
    anticipate = get_object_or_404(Anticipate, pk=id)
    payment = get_object_or_404(Payment, pk=anticipate.payment_id)
    
    #Change status
    if new_status == 'accepted':
        anticipate.status = 'accepted'
        payment.status = 'accepted'
        payment.original_value = anticipate.original_value
        payment.original_value = anticipate.new_value
        payment.old_due_date = payment.due_date
        payment.due_date = anticipate.new_due_date
        payment.save()
        anticipate.save()
        # Add to log
        logger.info(f'operator {request.user.id} changed anticipate {id} status to accepted')
        logger.info(f'Changed payment {anticipate.payment_id} status to accepted')
        # Send email to user
        send_email(request, payment=payment, subject='accepted')
        #Show message to user
        messages.info(request, 'Status changed to "accept" sucessfully')
    elif new_status == 'denied':
        anticipate.status = 'denied'
        payment.status = 'denied'
        anticipate.save()
        payment.save()
        # Add to log
        logger.info(f'operator {request.user.id} changed anticipate {id} status to denied')
        logger.info(f'Changed payment {anticipate.payment_id} status to denied')
        # Send email to user
        send_email(request, payment=payment, subject='denied')
        # Show messahe to user
        messages.info(request, 'Status changed to "denied" sucessfully')
    else:
        #Invalid option
        messages.error(request, 'Invalid Status Option')

    return redirect(f'/anticipate/{anticipate.id}')


@login_required
def anticipate_request_view(request, id):
    """Request anticipate payment"""

    #Check if user has permission to see this page
    if not check_group(request=request, group='fornecedores'):
        return render_not_allowed(request)

    #get payment
    payment = get_object_or_404(Payment, pk=id, provider=request.user)
    logger.info(f'Verify anticipate request to payment {payment.id}')

    #Check if can anticipate the payment 
    if not check_can_anticipate(payment=payment):
        return render_not_allowed(request)

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
    logger.info(f'Added new anticipate to db, id: {new_anticipate.id}')
    # Send email to user
    send_email(request, payment=payment, subject='request')
    messages.info(request, 'Anticipate request done')
    #Return to home
    return redirect('/')


@login_required
def anticipate_info_view(request, id):
    """Calculate antecipated info about a payment"""

    #Check if user has permission to see this page
    if not check_group(request=request, group='fornecedores'):
        return render_not_allowed(request)

    payment = get_object_or_404(Payment, pk=id)

    if payment.paid == False:
        original_value, new_value, original_due_date, new_due_date, days_delta = get_antecipate_value(payment=payment)
        return render(request, 'payments/anticipate_payment_view.html', {'payment': payment, 'original_value': original_value, 'new_value': new_value, 'original_due_date': original_due_date, 'new_due_date': new_due_date, 'days_delta':days_delta})


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

    logger.info(f'get anticipate info to payment {payment.id}')
    return original_value, new_value, original_due_date, new_due_date, days_delta


def check_group(request, group) -> bool:
    """
    Check if user is in the group.

    Return False if user is not in the group
    """
    user_groups = list(request.user.groups.values_list('name', flat = True))
    logger.info(f'Check user {request.user.id} groups')
    return group in user_groups


def render_not_allowed(request):
    """Render Not allowed page """
    logger.info(f'user: {request.user.id} with the groups {list(request.user.groups.values_list("name", flat = True))} tried to access unauthorized url')

    return render(request, 'payments/not_allowed.html', {'not': 'allowed'})


def check_can_anticipate(payment) -> bool:
    """Check if a payment can be anticipated verifying due_date"""
    logger.info(f'Check if payment {payment.id} can be anticipated')
    return payment.due_date >= datetime.date.today()



