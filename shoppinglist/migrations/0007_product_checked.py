# Generated by Django 4.2.4 on 2023-08-18 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppinglist', '0006_list_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
