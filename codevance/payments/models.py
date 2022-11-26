from django.db import models
from django.contrib.auth import get_user_model


def get_sentinel_user():
    """
    Create 'deleted' user to replace when some user is erased
    """
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Payment(models.Model):
    
    #Valid option to status fiels
    STATUS = (
        ('not_requested', 'Not Requested'),
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('denied', 'Denied'),
    )

    emission_date = models.DateField()
    due_date = models.DateField()
    payment_date = models.DateField(null=True)
    original_value = models.DecimalField(max_digits=14, decimal_places=2)
    paid = models.BooleanField(default=False)
    status = models.TextField(max_length=20, choices=STATUS, default='not_requested')
    provider = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user))
    provider_social_reason = models.TextField(max_length=100)
    provider_cnpj = models.TextField(max_length=25)


    def __str__(self):
        return f'{self.id} - {self.provider_social_reason} -> {self.due_date}, R$ {self.original_value} Status: {self.status}'




