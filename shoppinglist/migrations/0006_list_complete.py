# Generated by Django 4.2.4 on 2023-08-18 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppinglist', '0005_remove_list_product_product_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
