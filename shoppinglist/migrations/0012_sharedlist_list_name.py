# Generated by Django 4.2.4 on 2023-08-19 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppinglist', '0011_alter_list_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharedlist',
            name='list_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]