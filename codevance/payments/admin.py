from django.contrib import admin

# Register your models here.

from .models import Payment, Anticipate

admin.site.register(Payment)
admin.site.register(Anticipate)

