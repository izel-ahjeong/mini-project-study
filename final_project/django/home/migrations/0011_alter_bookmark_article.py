# Generated by Django 3.2.12 on 2024-05-09 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_bookmark_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.article'),
        ),
    ]