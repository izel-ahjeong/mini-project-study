# Generated by Django 4.1.12 on 2024-05-02 02:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_users_info_user_age_keywords_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users_info',
            name='user_age_keywords',
        ),
        migrations.RemoveField(
            model_name='users_info',
            name='user_custom_keywords',
        ),
    ]
