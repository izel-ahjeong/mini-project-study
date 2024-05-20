from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from account.models import Users_info
from django.db.models import Avg
from django.contrib.auth.models import User
from .models import Article, Category, Bookmark, Rating, User_Article_Rating_TB, User_Article_Bookmark_TB, age_recommand_Article_TB
from django.http import HttpResponse

import requests
import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from django_pandas.io import read_frame
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from .utils import timezone, filter_age_range, preprocess_and_extract_topics, extract_keywords, extract_words, recommend_similar_articles, user_custom_extract_topics, user_custom_recommendation_similar_articles, clean_text, generate_wordcloud_data
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
stop_words = set(stopwords.words('english'))

# 자동
from django.views import View
import schedule
import time
import requests


# 워드클라우드 
from wordcloud import WordCloud   # pip install wordcloud
import matplotlib.pyplot as plt
import io
import base64



# 비회원 전용 홈페이지
@require_safe
def logged_out_list(request):
    # 최신 기사 6개
    latest_articles = Article.objects.all().order_by('-article_public_Date')[:6]

    context = {
        'latest_articles': latest_articles,
    }

    # 템플릿 렌더링
    return render(request, 'home/logged_out_index.html', context)



# 로그인 전용 홈페이지
@login_required
@require_safe
def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category_articles = Article.objects.filter(category=category).order_by('-article_public_Date')
    categories = Category.objects.all()
    
    latest_articles = Article.objects.all().order_by('-article_public_Date')[:6]
    
    # 기사별 평균 평점 계산
    # 뻘짓 조심: 카테고리로 나눴다는 걸 생각을 안하고 있었음. 그래서 새로운 함수로 평점을 계산해도 템플릿은 {% for article in category_articles %}을 사용하기에 보여지지도 않았던 거였음..ㅠ
    for article in category_articles:
        article.average_rating = article.rating_set.aggregate(avg_rating=Avg('ratings'))['avg_rating']
    
    # 페이지네이션
    paginator = Paginator(category_articles, 10)  # 페이지당 10개의 기사를 보여줌
    page = request.GET.get('page')

    if page is None:
        page = 1
    else:   
        try:
            page = int(page)
        except ValueError:
            page = 1
    
    try:
        category_articles = paginator.page(page)
    except PageNotAnInteger:
        # 페이지가 정수가 아닌 경우, 첫 번째 페이지를 반환
        category_articles = paginator.page(1)
    except EmptyPage:
        # 페이지가 범위를 벗어난 경우, 마지막 페이지를 반환
        category_articles = paginator.page(paginator.num_pages)  

    leftIndex = (int(page) - 2) 
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 2)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex, rightIndex+1)

    # 유사 기사 추천
    age_recommand_articles = age_recommand_Article_TB.objects.all()
    # 최신기사 150개 유사도 분석
    new_articles = Article.objects.all().order_by('-article_public_Date')[:150]
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([user_tag.tag for user_tag in age_recommand_articles])

    recommended_articles = recommend_similar_articles(age_recommand_articles, new_articles, tfidf_vectorizer, tfidf_matrix)
    

    # 워드클라우드 단어 리스트 
    recent_articles_for_word_cloud = Article.objects.filter(category_id=category_id).order_by('-article_public_Date')[:60]
    word_freq_dict = generate_wordcloud_data(recent_articles_for_word_cloud)

    # 워드클라우드 이미지 생성
    wordcloud= WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq_dict)
    plt.figure(figsize=(8,4))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)

    # 이미지를 바이트로 변환하여 임시 메모리에 저장
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # 바이트로 변환된 이미지를 base64로 인코딩하여 HTML 에 직접 포함
    image_base64 = base64.b64encode(image_stream.getvalue()).decode()

    return render(
        request,
        "home/logged_index.html",
        {
            "category_name": category.name,  # 카테고리 이름을 템플릿으로 전달
            "category_articles": category_articles,
            "categories": categories,
            "latest_articles": latest_articles,
            "custom_range": custom_range,
            "recommended_articles": recommended_articles,
            "wordcloud_image": f"data:image/png;base64,{image_base64}",
        },
    )

# 활동관리 페이지
@login_required
@require_safe
def activity_management(request):
    return render(request, 'home/activity_management.html')


# 연령별 핵심토픽 업데이트
# 일주일에 한번 돌아가기
def process_data(request):
    # 연령대별 데이터프레임 생성
    age_ranges = [(10, 20), (20, 30), (30, 40), (40, 50), (50, 60)]
    age_df_list = [filter_age_range(User_Article_Rating_TB.objects.all(), age_range) for age_range in age_ranges]

    # 연령대별 가중치, 불용어처리 및 핵심 토픽 추출
    topics_age_list = []
    for age_df in age_df_list:
        result_age_df = preprocess_and_extract_topics(age_df)
        topics_age_df = extract_words(extract_keywords(result_age_df['processed_abstract']))
        topics_age_list.append(topics_age_df)

    # 데이터베이스에 저장
    for i, topics_age in enumerate(topics_age_list):
        # 연령대를 새로 추가할때
        age_instance, created = age_recommand_Article_TB.objects.get_or_create(age=10 * (i+1))
        # 기존 연령대의 tag만 업데이트
        if not created:  
            age_instance.tag = topics_age
            age_instance.save()







