# Generated by Django 4.1.3 on 2022-11-26 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_payment_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.TextField(choices=[('not_requested', 'Not Requested'), ('requested', 'Requested'), ('accepted', 'Accepted'), ('denied', 'Denied')], default='not_requested', max_length=20),
        ),
    ]
