# Generated by Django 4.1.12 on 2024-05-01 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_new_article_tb'),
    ]

    operations = [
        migrations.CreateModel(
            name='age_recommand_Article_TB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(verbose_name='나이')),
                ('tag', models.TextField()),
            ],
        ),
    ]