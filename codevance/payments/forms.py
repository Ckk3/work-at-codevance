from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    
    class Meta:
        model = Payment
        fields = ('emission_date', 'due_date', 'value', 'provider_social_reason', 'provider_cnpj')
