# Generated by Django 3.2 on 2021-07-20 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_customer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, default=1, upload_to=''),
            preserve_default=False,
        ),
    ]