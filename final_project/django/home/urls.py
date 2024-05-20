from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
    # home/
    # 로그아웃 전용 홈페이지
    path('', views.logged_out_list, name='logged_out_list'),

    # home/category/1
    # 로그인 전용 홈페이지
    path('category/<int:category_id>/', views.category_view, name='category'),

    #home/1/activity_management/
    path('activity_management/', views.activity_management, name='activity_management'),

]

