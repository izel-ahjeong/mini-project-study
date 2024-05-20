import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from django.db.models.query import QuerySet
from django.utils import timezone


# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
stop_words = set(stopwords.words('english'))


# 워드 클라우드 전용 라이브러리
nltk.download('wordnet')
import re
from nltk import pos_tag, word_tokenize
from collections import Counter





# 연령대별 필터링
def filter_age_range(queryset, age_range):
    min_age, max_age = age_range
    # QuerySet을 리스트로 변환
    queryset_list = list(queryset.values())
    # pandas DataFrame으로 변환
    age_df = pd.DataFrame(queryset_list)
    # 나이에 대한 필터링
    age_df = age_df[(age_df['user_age'] >= min_age) & (age_df['user_age'] < max_age)]
    return age_df

# 가중치계산
def bayesian_average(ratings, confidence=0.95):
    num_ratings = len(ratings)
    avg_rating = np.mean(ratings)
    bayesian_avg = (confidence * 2 + num_ratings * avg_rating) / (confidence + num_ratings)
    return bayesian_avg

# 가중치를 받은뒤 중복 아티클 제거 그리고 3.5이상만 가져오기
def preprocessing(df):
    average_ratings = df.groupby('article_id')['ratings'].agg(bayesian_average).reset_index()
    unique_articles = df.drop_duplicates(subset='article_id', keep='first')
    unique_articles = unique_articles.merge(average_ratings, on='article_id', suffixes=('_original', '_average'))
    require_col = unique_articles[['article_id', 'abstract', 'article_public_Date', 'ratings_average']]
    require_col = require_col[require_col['ratings_average'] >= 3.5]
    return require_col


# 불용어 처리
def processed_abstract(text):
    words = word_tokenize(text)
    tagged_words = pos_tag(words)
    nouns = [word for word, pos in tagged_words if pos.startswith('NN') and word.lower() not in stop_words]
    processed_text = ' '.join(nouns)
    return processed_text

# 불용어를 제거한걸 열에붙이
def extract_topics(df):
    df['processed_abstract'] = df['abstract'].apply(processed_abstract)
    return df

def preprocess_and_extract_topics(df):
    # Bayesian 평균 계산 및 필터링
    df = preprocessing(df)

    # 토픽 추출을 위한 단어 처리
    df = extract_topics(df)

    return df

# 연령대별 핵심 토픽 추출
def extract_keywords(text):
    # TF 벡터화
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english', token_pattern=r'\b[^\d\W_]{3,}\b')
    tf = vectorizer.fit_transform(text)
    # LDA 모델링
    lda_model = LatentDirichletAllocation(n_components=9, max_iter=5, learning_method='online', learning_offset=50., random_state=0)
    lda_model.fit(tf)
    # 각 연령대별로 핵심 토픽 추출
    topics = []
    for topic_idx, topic in enumerate(lda_model.components_):
        top_words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]
        topics.append((topic_idx, top_words))
    return topics

# 연령대별 핵심단어 나열
def extract_words(topics):
  words = []
  for topic in topics:
    for word in topic[1]:
      words.append(word)
  return ' '.join(words[:])

# 연령대별 새로운 기사 추천
def recommend_similar_articles(user_tags, new_articles, tfidf_vectorizer, tfidf_matrix):
    recommended_articles = []

    for user_tag in user_tags:
        user_tfidf = tfidf_vectorizer.transform([user_tag.tag])

        similarities = cosine_similarity(user_tfidf, tfidf_vectorizer.transform([article.content for article in new_articles]))

        similar_articles_indices = similarities.argsort()[0][::-1]
        recommended_articles_indices = similar_articles_indices[:5]
        recommended_articles_df = [new_articles[int(i)] for i in recommended_articles_indices]
        
        # 연령
        recommended_articles_with_age = {"user_age": user_tag.age, "articles": recommended_articles_df}
        recommended_articles.append(recommended_articles_with_age)

    return recommended_articles



# 전처리 함수
# NLTK의 WordNetLemmatizer를 사용하여 어근 변환 함수 작성
def lemmatize_token(text):
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(word) for word in text.lower().split()])

# 사용자 정의 함수를 포함한 함수 체인 구성
def preprocess(text):
    return lemmatize_token(text)



# 북마크 기반 개인 맞춤형 토픽 추출
def user_custom_extract_topics(text):

    # TF 벡터화
    count = CountVectorizer(max_df = 0.95, stop_words="english", preprocessor=preprocess ,token_pattern=r'\b[^\d\W_]{3,}\b')
    count_vectored = count.fit_transform(text)
    feature_names = count.get_feature_names_out()

    # LDA 모델링

    lda = LatentDirichletAllocation(n_components=15, random_state=11, learning_method="batch")
    lda.fit(count_vectored)

    topics = []
    for topic_index, topic in enumerate(lda.components_):

        topic_word_indexes = topic.argsort()[::-1]
        top_indexes = topic_word_indexes[ :10]

        feature_concat = ' '.join([feature_names[i] for i in top_indexes])
        topics.append(feature_concat)

    topics = [','.join(topics)]
    return topics


# 사용자별 추천 기사 5개
def user_custom_recommendation_similar_articles(topics, new_article_df):
    recommended_articles = []

    # t사용자(키워드)에 대해서 오늘 들어온 기사들과 유사도 기반 추천 기사 찾기
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(topics)  # 사용자의 관심사 TF-IDF 벡터

    # 새로운 기사들과의 유사도 계산
    similarities = cosine_similarity(tfidf_matrix, tfidf_vectorizer.transform(new_article_df.values_list('content', flat=True)))

    # 유사도가 높은 순 추천
    similar_articles_indices = similarities.argsort()[0][::-1]
    recommended_articles_indices = similar_articles_indices[:5]  # 상위 5개 기사
    # recommended_articles_df = new_article_df.iloc[recommended_articles_indices]
    recommended_articles_df = [new_article_df[int(i)] for i in recommended_articles_indices]

    recommended_articles.append(recommended_articles_df)

    return recommended_articles





# 워드 클라우드 함수
# 전처리 함수 1
def clean_text(text):
    stop_words = set(stopwords.words("english"))
    # 원하는 단어를 불용어로 추가
    stop_words.update(['world', "people", "year",'player','day',"time", "thing", "way", "something", "business", "technology", "game", "team", "life", 'work', 'point'])

    text = text.lower()
    # 숫자, 특수문자를 빈 문자열로 대체
    text = re.sub(r'\W+|\d+', ' ', text)
    # 단어가 3글자 이하이면 빈 문자열로 대체
    text = re.sub(r'\b\w{1,2}\b', '', text)
    # 불용어 제거
    text = [word for word in text.split() if word not in stop_words]

    text = ' '.join(text)
    return text

# 워드 클라우드 전처리 2
def generate_wordcloud_data(articles):
    text = ' '.join([clean_text(article.content) for article in articles])

    # nltk 의 품사 태깅을 이용하여 명사 추출
    # 단어 토큰화 및 품사 태깅
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)

    # 명사만
    nouns_adjs = [word for word, tag in tags if tag.startswith('N')]

    counts = Counter(nouns_adjs)
    tags = counts.most_common(60)

    word_freq_dict = {word: freq for word, freq in tags}
    return word_freq_dict