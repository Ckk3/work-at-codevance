from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


def get_sentinel_user():
    """
    Create 'deleted' user to replace when some user is erased
    """
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Payment(models.Model):
    

    emission_date = models.DateTimeField()
    due_date = models.DateTimeField()
    original_value = models.DecimalField(max_digits=14, decimal_places=2)
    provider = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user))
    provider_social_reason = models.TextField(max_length=100)
    provider_cnpj = models.TextField(max_length=25)




