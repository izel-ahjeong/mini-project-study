# Generated by Django 4.1.12 on 2024-05-02 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_users_info_user_age_keywords_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users_info',
            name='user_age_keywords',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users_info',
            name='user_custom_keywords',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
