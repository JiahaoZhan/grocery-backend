# Generated by Django 4.2.4 on 2023-08-17 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppinglist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='color',
            field=models.CharField(default='', max_length=255),
        ),
    ]
