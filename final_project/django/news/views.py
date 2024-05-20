from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from home.models import Article, Comment, Bookmark, Rating, User_Article_Rating_TB, User_Article_Bookmark_TB
from account.models import Users_info

from news.forms import CommentForm, RatingForm
from django.urls import reverse
# Create your views here.
# def news_detail(request, article_pk):
#     article = get_object_or_404(Article, pk=article_pk)

# 뉴스 내용 보여주기
def news_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    comment_form = CommentForm()
    rating_form = RatingForm()
    is_bookmark = article.bookmark_set.filter(user=request.user.pk).exists()
    return render(request, "news/news_detail.html", {"article" : article,
                                                     "comment_form" : comment_form,
                                                     "rating_form" : rating_form,
                                                     "is_bookmark" : is_bookmark
                                                    })



# 댓글 작성 로직
@login_required
def news_comment_create(request, article_id):
    form = CommentForm(request.POST)
    article = get_object_or_404(Article, pk=article_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.article = article
        comment.save()
    return redirect("news:news_detail", article.pk)



# 북마크 생성 및 삭제 로직
@login_required
def news_bookmarked(request, article_id):
    if request.method == "POST":
        article = Article.objects.get(pk = article_id)
        user = request.user

        # 사용자가 북마크 누른 객체 가져오기
        bookmarked_article = user.bookmark_set.filter(article = article)
        bookmarked_article_user = user.user_article_bookmark_tb_set.filter(article=article)

        # 만약 사용자가 북마크 누른 기사가, 북마크 누른 기사 목록들에 있다면 삭제
        if bookmarked_article.exists():
            bookmarked_article.delete()
            if bookmarked_article_user.exists():
                bookmarked_article_user.delete()
        else:
            user.bookmark_set.create(user=user, article=article)

            # user_article_rating_tb
            user_info = user.users_info_set.first()  # 사용자 정보 가져오기
            if user_info:
                user_age = user_info.user_age  # 사용자의 나이 가져오기
            else:
                user_age = None  # 사용자 정보가 없는 경우 처리
            abstract = article.abstract
            category = article.category
            User_Article_Bookmark_TB.objects.create(user=user, user_age=user_age, article=article, abstract=abstract, category=category,  )


    return redirect("news:news_detail", article.pk)


# 평점
@login_required
def news_rating(request, article_id):
    if request.method == "POST":
        article = Article.objects.get(pk=article_id)
        user = request.user
        new_rate = float(request.POST.get("ratings"))  # 사용자가 선택한 새로운 평점 가져오기

        # 사용자가 해당 기사에 대해 이미 평가한 평점이 있는지 확인
        rated_article = user.rating_set.filter(article=article)
        rated_article_user = user.user_article_rating_tb_set.filter(article=article)

        # 만약 이미 평점이 존재한다면 업데이트
        if rated_article.exists():
            rated_article.update(ratings=new_rate)
            if rated_article_user.exists():
                rated_article_user.update(ratings=new_rate)
        else:
            # 새로운 평점 생성
            rating_instance = Rating.objects.create(user=user, article=article, ratings=new_rate)

            # User_Article_Rating_TB에도 동일한 평점 생성
            user_info = user.users_info_set.first()  # 사용자 정보 가져오기
            if user_info:
                user_age = user_info.user_age  # 사용자의 나이 가져오기
            else:
                user_age = None  # 사용자 정보가 없는 경우 처리
            abstract = article.abstract
            article_public_Date = article.article_public_Date
            User_Article_Rating_TB.objects.create(user=user, user_age=user_age, article=article, ratings=new_rate, abstract=abstract, article_public_Date=article_public_Date)

    return redirect("news:news_detail", article_id)


# 사용자별 북마크 리스트
@login_required
def bookmark_list(request, user_pk):
    # 현재 로그인한 사용자의 댓글 목록
    user_bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'news/bookmark_list.html', {'user_bookmarks': user_bookmarks})


# 북마크 삭제
@login_required
def bookmark_delete(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, id=bookmark_id)

    # 북마크 삭제하면 User_Article_Bookmark_TB에 있는 북마크 데이터도 삭제될수 있도록 하기
    User_Article_Bookmark_TB.objects.filter(article_id=bookmark.article.id, user_id=request.user.id).delete()
    
    # 북마크 삭제 처리
    bookmark.delete()
    
    # 북마크 삭제 후 댓글 리스트 페이지로 리디렉션
    return redirect(reverse('news:bookmark_list', kwargs={'user_pk': request.user.pk}))


# 사용자별 댓글 리스트
@login_required
def comment_list(request, user_pk):
    # 현재 로그인한 사용자의 댓글 목록
    user_comments = Comment.objects.filter(user=request.user)
    return render(request, 'news/comment_list.html', {'user_comments': user_comments})

# 댓글 삭제
@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # 댓글 삭제 처리
    comment.delete()
    
    # 댓글 삭제 후 댓글 리스트 페이지로 리디렉션
    return redirect(reverse('news:comment_list', kwargs={'user_pk': request.user.pk}))




