from django.db import models
from django.conf import settings

# 회원 상세정보 받기
class Users_info(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_age = models.IntegerField(verbose_name="나이")

    # 지역 선택
    REGION_CHOICES = [
        ('seoul', '서울'),
        ('gyeonggi', '경기'),
        ('gangwon', '강원'),
        ('chungbuk', '충북'),
        ('chungnam', '충남'),
        ('jeonbuk', '전북'),
        ('jeonnam', '전남'),
        ('gyeongbuk', '경북'),
        ('gyeongnam', '경남'),
        ('jeju', '제주')
    ]
    user_region = models.CharField(max_length=10, choices=REGION_CHOICES, verbose_name="지역")

    # 성별 선택
    SEX_CHOICES = [
        ('male', '남'),
        ('female', '여')
    ]
    user_sex = models.CharField(max_length=10, choices=SEX_CHOICES, verbose_name="성별")

    # 직업 선택
    JOB_CHOICES = [
        ('student', '학생'),
        ('worker', '직장인'),
        ('unemployed', '취업준비 중'),
        ('others', '기타')
    ]
    user_job = models.CharField(max_length=10, choices=JOB_CHOICES, verbose_name="직업")

    # 가입 목적 선택
    PURPOSE_CHOICES = [
        ('hobby', '취미'),
        ('investment', '주식투자'),
        ('none', '없음')
    ]
    user_purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES, verbose_name="가입 목적")

    class Meta:
        db_table = 'tb_users_info'
    

    def __str__(self):
        return f"{self.user_id.username} 의 상세정보"
    