# Generated by Django 3.2 on 2021-07-20 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_customer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='orders',
        ),
    ]
