# Generated by Django 3.2 on 2021-04-12 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rename_customers_customer'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
    ]
