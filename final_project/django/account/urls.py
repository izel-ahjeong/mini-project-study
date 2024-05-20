from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    #account/signup/
    path('signup/', views.signup, name='signup'),

    #account/1/signup_info/
    path('<int:user_pk>/signup_info/', views.signup_info, name='signup_info'),

    #account/1/user_info/
    path('<int:user_pk>/user_info/', views.user_info, name='user_info'),

    #account/1/update_user_info/
    path('<int:user_pk>/update_user_info/', views.update_user_info, name='update_user_info'),

    # account/login/
    path('login/', views.login, name='login'),
 
    # account/logout/
    path('logout/', views.logout, name='logout'),

    # account/1/mypage/
    path('<int:user_pk>/mypage/', views.mypage_recomm_and_bookmark, name='mypage_recomm_and_bookmark'),

    # account/delete_account
    path('delete_account/', views.delete_account, name='delete_account'),
]

