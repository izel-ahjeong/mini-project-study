# Generated by Django 4.1.12 on 2024-04-12 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users_info',
            name='user_password',
        ),
    ]