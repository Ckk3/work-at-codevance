from django.test import TestCase
from payments.models import Payment, Anticipate
from django.contrib.auth.models import User
from payments.forms import PaymentForm


class TestUsers(TestCase):
    
    def test_create_fornecedor(self):

        forn = User.objects.create(username='forn1', password='123456')

        self.assertTrue(isinstance(forn, User))
    
    def test_create_form(self):
        data = {
            'emission_date': '2022-10-12',
            'due_date': '2022-10-12',
            'value': 1425,
            'provider_social_reason':'Social Rewaosn',
            'provider_cnpj':'31231234'
        }
        form = PaymentForm(data=data)
        self.assertTrue(form.is_valid())



