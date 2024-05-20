"""
Django settings for ksc_project project.

Generated by 'django-admin startproject' using Django 4.1.12.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p0qb=yf36#2ce3w2jliw2*%rx3b%gw+f9pk9&4oa!l#mde-c7m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['54.249.233.132', 'ec2-54-249-233-132.ap-northeast-1.compute.amazonaws.com']
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '54.249.233.132']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'django_seed',
    'django_crontab',
    
    "account", # 회원가입, 로그인, 회원 정보, 로그아웃, 마이페이지, 탈퇴
    "home", # 메인 홈페이지, 활동 관리 페이지(북마크, 리뷰)
    "news", # 댓글, 북마크, 평점 작성 및 삭제, 기사 원문

    'ksc_project',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ksc_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ksc_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'django_dataset',
       'USER': 'USERNAME',
       'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
       'HOST': '127.0.0.1',
       'PORT': 3306,
   }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MySQL을 브로커로 사용하는 경우
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'

# 작업 결과를 MySQL에 저장하는 경우
CELERY_RESULT_BACKEND = 'db+mysql://USERNAME:multi1234!!@localhost/django_dataset'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'

# 연령대 추천모델에 필요함
# home/views.py/process_data 함수를 매주 일요일 자정에 실행
# CRONJOBS = [
#     ('0 0 * * 0', 'home.views.process_data'),
#     ('*/1 * * * *', '/bin/bash -c "source /home/ubuntu/miniconda3/envs/django-env/bin/activate && python /home/ubuntu/django/ksc_project/manage.py shell -c \'import home.views; home.views.telegram_message(request)\'"'),
#     ('*/1 * * * *', 'cd /home/ubuntu/django/ksc_project && /home/ubuntu/miniconda3/envs/django-env/bin/python /home/ubuntu/django/ksc_project/manage.py shell -c "from home.views import telegram_message; telegram_message()"')
# ]
# ('25 2 * * *', '/home/ubuntu/miniconda3/envs/django-env/bin/python /home/ubuntu/django/ksc_project/manage.py shell -c "import home.views; home.views.telegram_message()"'),
# ('33 2 * * *' , './home/ubuntu/miniconda3/bin/activate && /home/ubuntu/miniconda3/envs/django-env/bin/python /home/ubuntu/django/ksc_project/manage.py shell -c' "import home.views; home.views.telegram_message()"),
# */1 * * * * cd /home/ubuntu/django/ksc_project && /home/ubuntu/miniconda3/envs/django-env/bin/python /home/ubuntu/django/ksc_project/manage.py shell -c "from home.views import telegram_message; telegram_message()" 


# 세션 쿠키의 유효 기간(초)
# SESSION_COOKIE_AGE = 1200

# 브라우저를 닫을 때 세션을 만료
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_ENGINE = 'django.contrib.sessions.backends.db'