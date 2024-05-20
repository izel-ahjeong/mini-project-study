from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # 기사 페이지 domain/news/1/
    path('<int:article_id>/', views.news_detail, name="news_detail"),

    # 기사 페이지 댓글 작성 기능  domain/news/1/artcle-comment-create-function/
    path('<int:article_id>/artcle-comment-create-function/', views.news_comment_create, name="news_comment_create"),

    # 기사 북마크 (좋아요) 처리 기능  domain/news/1/bookmarked-fuction/
    path("<int:article_id>/bookmarked-fuction/", views.news_bookmarked, name="news_bookmarked"),
    
    # 기사 평점 기능  domain/news/1/rating-function/
    path("<int:article_id>/rating-function/", views.news_rating, name="news_rating"),
    
    # 북마크 목록 news/1/bookmark_list
    path("<int:user_pk>/bookmark_list/", views.bookmark_list, name="bookmark_list"),  

    # 북마크 삭제 news/bookmark_delete/1
    path('bookmark_delete/<int:bookmark_id>/', views.bookmark_delete, name='bookmark_delete'),
   
    # 댓글 목록 news/1/comment_list
    path("<int:user_pk>/comment_list/", views.comment_list, name="comment_list"),  

    # 댓글 삭제 news/comment_delete/1
    path('comment_delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]
