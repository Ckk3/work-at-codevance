import pytest
from payments.models import Payment, Anticipate
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestUsers:
    pytestmark = pytest.mark.django_db
    
    @pytest.mark.django_db
    def test_admin_superuser(self):
        admin = User.objects.get(username='admin')
        assert admin.is_superuser

    @pytest.mark.django_db
    def test_fornecedor1_superuser(self):
        forn = User.objects.get(username='forn1')
        assert forn.is_superuser == False

    @pytest.mark.django_db
    def test_fornecedor2_superuser(self):
        forn = User.objects.get(username='forn2')
        assert forn.is_superuser == False

    @pytest.mark.django_db
    def test_operador_superuser(self):
        ope = User.objects.get(username='ope')
        assert ope.is_superuser == False

    @pytest.mark.django_db    
    def test_fornecedor1_ingroup(self):
        forn = User.objects.get(username='forn1')
        user_groups = list(forn.groups.values_list('name', flat = True))
        assert 'fornecedores' in user_groups




