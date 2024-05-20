from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_safe
from django.contrib.auth.decorators import login_required

# 기본적으로 form 사용할거면 이거 쓰면 됨.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .forms import Users_infoForm

from .models import Users_info
from home.models import Article, Bookmark, User_Article_Bookmark_TB
from django.http import HttpResponseForbidden

import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity

from home.utils import timezone, user_custom_extract_topics, user_custom_recommendation_similar_articles


@require_http_methods(["GET", "POST"])
def signup(request):
    # 만약 가입한 사용자가 또 가입을 하러온다면 막아야 함
    # if request.user.is_authenticated:
    #     return redirect("board:article_index")
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 회원 등록
            user = form.save()
            # 바로 이어서 로그인 시켜주기
            auth_login(request, user)
            user_pk = user.pk
            return redirect("account:signup_info", user.pk)
    else:
        form = UserCreationForm()
    return render(request, "account/signup.html", {
        'form' : form,
    })

def signup_info(request, user_pk):
    if request.method == "GET":
        form = Users_infoForm()
        return render(request, 'account/signup_info.html', 
                      {'form':form, 'user_pk': user_pk})

    elif request.method == "POST":
        user = get_object_or_404(User, pk=user_pk)
        form = Users_infoForm(request.POST)
        if form.is_valid():
            info_form = form.save(commit=False)
            info_form.user_id = request.user
            info_form.save()
            return redirect("home:category", category_id=1)



# 내 회원 정보 확인
# user_info.html에서 수정하기 버튼을 누르면 account:update_user_info로 redirect
def user_info(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user_info = Users_info.objects.get(user_id_id=user)
    form = Users_infoForm()
    return render(request, 'account/user_info.html', {'user_info': user_info})

    
# 회원 정보 수정
# 수정완료 후 다시 account:user_info로 redirect
@login_required
@require_http_methods(["GET", "POST"])
def update_user_info(request, user_pk):
    user_info = get_object_or_404(Users_info, user_id=user_pk)
    # 지금 요청 보낸 너가 글쓴이가 아니라면
    if request.method == "POST":
        form = Users_infoForm(request.POST, instance=user_info) 
        if form.is_valid():
            form.save()
            return redirect("account:user_info", user_pk=user_pk)
    else:
        form = Users_infoForm(instance=user_info)    
    # elif request.method == 'GET':
    #     form = Users_infoForm(instance=info)
            # 폼이 유효하지 않은 경우에는 다시 폼을 보여줌
    return render(request, 'account/update_user_info.html', {'form': form, 'user_pk': user_pk})



@require_http_methods(["GET", "POST"])
def login(request):
    # 만약 로그인한 사용자가 또 로그인을 하러온다면 막아야 함
    if request.user.is_authenticated:
        return redirect("home:category", category_id=1)
    
    elif request.method == "POST":
        # AuthenticationForm 은 다른 modelform 들과는 다르다. 이건 modelform 이 아님
        form = AuthenticationForm(request, data=request.POST)  # 걍 이렇게 써야함
        if form.is_valid():
            user = form.get_user()  # form 이 유효하면, get user 객체를 통해 user 를 가져올 수 있다
            # 로그인 시켜주기 (저장의 개념이 아님)
            auth_login(request, user)
            username = user.username
            return redirect("home:category", category_id=1)
    else:
        form = AuthenticationForm()
    return render(request, "account/login.html", {
        "form" : form,
    })


# 로그아웃
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home:logged_out_list')



# 마이페이지
@login_required
def mypage_recomm_and_bookmark(request, user_pk):
    # 북마크 리스트 보여주기
    user = User.objects.get(id=user_pk)
    bookmark_articles = Bookmark.objects.filter(user = user)


    # 추천 기사 보여주기
    user = request.user

    # 갓 회원가입한 사람이라 북마크 갯수가 20개 이하면 추천 함수 실행 X
    if User_Article_Bookmark_TB.objects.filter(user=user).count() < 20 :
        recommend_articles_df = None
    else:
        user_abstracts  = User_Article_Bookmark_TB.objects.filter(user = user).order_by('-id').values_list('abstract', flat=True)[:30]  # 북마크한 데이터 중 최근 30개 데이터만 갖고 추천시스템 적용
        # value_list 함수는 특정 사용자의 abstract 값들을 [] 리스트 형태로 가져옴  ['This is the abstract of article 1', 'This is the abstract of article 2', ..]
        # 유저의 토픽들이 리스트 안에 들어있는 상태
        user_topics = user_custom_extract_topics(user_abstracts)

        # 새기사 가져와야 함
        # 이미 북마크 누른 객체들의 id 값들을 리스트로 가져오기
        user_bookmarked_ids = User_Article_Bookmark_TB.objects.filter(user=user).values_list('article_id', flat=True)  #[2,3,4,...]

        # 가져온 리스트에 없는(exclude) id 값들 중 최근 30개에서 추천
        # new_articles = Article.objects.all().order_by('-article_public_Date')[:60] # 수정 전
        new_articles = Article.objects.exclude(id__in=user_bookmarked_ids).order_by('-article_public_Date')[:30]

        recommend_articles_df = user_custom_recommendation_similar_articles(user_topics,new_articles)[0]
        # print(recommend_articles_df)

    
    return render(request, "account/mypage.html", {"bookmark_articles" : bookmark_articles, 
                                                   'recommend_articles_df' : recommend_articles_df})


# 탈퇴기능
@login_required
def delete_account(request):
    if request.method == 'POST':
        # 사용자 계정 삭제
        request.user.delete()
        # 로그아웃
        logout(request)
        return redirect('home:logged_out_list')  # 탈퇴 후 홈페이지로 이동하거나 원하는 페이지로 이동할 수 있습니다.
    else:
        # POST 요청이 아닌 경우, 예외 처리 혹은 다른 처리 로직을 추가할 수 있습니다.
        pass