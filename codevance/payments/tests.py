from django.test import TestCase
from payments.models import Payment, Anticipate
from django.contrib.auth.models import User



class TestUsers(TestCase):
    
    def test_create_fornecedor(self):

        forn = User.objects.create(username='forn1', password='123456')

        self.assertTrue(isinstance(forn, User))
    
    # def test_fornecedor2_superuser(self):
    #     bah = User.objects.all()
    #     assert bah == True

    # def test_operador_superuser(self):
    #     ope = User.objects.get(username='ope')
    #     assert ope.is_superuser == False
        
    # def test_fornecedor1_ingroup(self):
    #     forn = User.objects.get(username='forn1')
    #     user_groups = list(forn.groups.values_list('name', flat = True))
    #     assert 'fornecedores' in user_groups



