# Generated by Django 4.1.12 on 2024-04-12 05:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Users_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_age', models.IntegerField(verbose_name='나이')),
                ('user_password', models.CharField(max_length=62, verbose_name='비밀번호')),
                ('user_region', models.CharField(choices=[('seoul', '서울'), ('gyeonggi', '경기'), ('gangwon', '강원'), ('chungbuk', '충북'), ('chungnam', '충남'), ('jeonbuk', '전북'), ('jeonnam', '전남'), ('gyeongbuk', '경북'), ('gyeongnam', '경남'), ('jeju', '제주')], max_length=10, verbose_name='지역')),
                ('user_sex', models.CharField(choices=[('male', '남'), ('female', '여')], max_length=10, verbose_name='성별')),
                ('user_job', models.CharField(choices=[('student', '학생'), ('worker', '직장인'), ('unemployed', '취업준비 중'), ('others', '기타')], max_length=10, verbose_name='직업')),
                ('user_purpose', models.CharField(choices=[('hobby', '취미'), ('investment', '주식투자'), ('none', '없음')], max_length=10, verbose_name='가입 목적')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tb_users_info',
            },
        ),
    ]
