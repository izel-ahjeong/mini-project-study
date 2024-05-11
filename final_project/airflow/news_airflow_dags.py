# conda install pytorch torchvision torchaudio cpuonly -c pytorch  (bertsum 을 사용하기 위한 torch 다운로드)
# pip install bert-extractive-summarizer
# pip install pandas
# pip install pytz
# pip install sentencepiece

from airflow import DAG


from datetime import datetime, timedelta
import pytz   # pip install 
import json
import requests
import pandas as pd  # pip install pandas

# 파이썬 커넥터
from airflow.operators.python import PythonOperator

# sql 저장을 위한 라이브러리
from sqlalchemy import create_engine

# bertsum 모델을 위한 라이브러리
from summarizer import Summarizer   # pip install bert-extractive-summarizer

# t5 모델을 위한 라이브러리
from transformers import AutoModelWithLMHead, AutoTokenizer


# 영국 시간대 설정
now = datetime.now(pytz.timezone("UTC"))
pst_now_date = now.strftime("%Y-%m-%d")

default_args = {'start_date' : datetime(2024,4,23),
                "retries" : 3,
                "retry_delay" : timedelta(minutes=5)}


# 공통 크롤링 함수
def guardian_search(your_section):
    my_api_key = "6de253c2-9d98-4b21-9750-e4e9b63c8d28"

    section = your_section

    url = "https://content.guardianapis.com/" + section
    final_url = url + "?from-date=" + pst_now_date + "&to-date=" + pst_now_date +"&show-fields=bodyText&page-size=200&api-key=" + my_api_key
    response = requests.get(final_url)
    news_data_json = response.content.decode("utf-8")

    # results 부분만 추출
    news_data_crawl = json.loads(news_data_json)
    news_data_crawl_results = news_data_crawl["response"]["results"]

    return news_data_crawl_results




# 각 section 별 크롤링 + 전처리 함수
# category : world

def is_world_crawl():
    world_crawl_data_origin = guardian_search("world")

    # results 에서 원하는 부분 추출 + key 값 이름 변경
    world_result_list = []

    for search_crawl_context in world_crawl_data_origin:
        world_result_dict = {}
        world_result_dict["article_public_Date"] = search_crawl_context["webPublicationDate"]
        world_result_dict['title'] = search_crawl_context["webTitle"]
        world_result_dict['content_url'] = search_crawl_context["webUrl"]
        world_result_dict['content'] = search_crawl_context["fields"]["bodyText"]
        world_result_dict["category_id"] = 1  # 카테고리는 번호로 부여
        world_result_list.append(world_result_dict)

    return world_result_list

def is_technology_crawl():
    technology_crawl_data_origin = guardian_search("technology")

    # results 에서 원하는 부분 추출 + key 값 이름 변경
    technology_result_list = []

    for search_crawl_context in technology_crawl_data_origin:
        technology_result_dict = {}
        technology_result_dict["article_public_Date"] = search_crawl_context["webPublicationDate"]
        technology_result_dict['title'] = search_crawl_context["webTitle"]
        technology_result_dict['content_url'] = search_crawl_context["webUrl"]
        technology_result_dict['content'] = search_crawl_context["fields"]["bodyText"]
        technology_result_dict["category_id"] = 2  # 카테고리는 번호로 부여
        technology_result_list.append(technology_result_dict)

    return technology_result_list

def is_business_crawl():
    business_crawl_data_origin = guardian_search("business")

    # results 에서 원하는 부분 추출 + key 값 이름 변경
    business_result_list = []

    for search_crawl_context in business_crawl_data_origin:
        business_result_dict = {}
        business_result_dict["article_public_Date"] = search_crawl_context["webPublicationDate"]
        business_result_dict['title'] = search_crawl_context["webTitle"]
        business_result_dict['content_url'] = search_crawl_context["webUrl"]
        business_result_dict['content'] = search_crawl_context["fields"]["bodyText"]
        business_result_dict["category_id"] = 3  # 카테고리는 번호로 부여
        business_result_list.append(business_result_dict)

    return business_result_list

def is_environment_crawl():
    environment_crawl_data_origin = guardian_search("environment")

    # results 에서 원하는 부분 추출 + key 값 이름 변경
    environment_result_list = []

    for search_crawl_context in environment_crawl_data_origin:
        environment_result_dict = {}
        environment_result_dict["article_public_Date"] = search_crawl_context["webPublicationDate"]
        environment_result_dict['title'] = search_crawl_context["webTitle"]
        environment_result_dict['content_url'] = search_crawl_context["webUrl"]
        environment_result_dict['content'] = search_crawl_context["fields"]["bodyText"]
        environment_result_dict["category_id"] = 4  # 카테고리는 번호로 부여
        environment_result_list.append(environment_result_dict)

    return environment_result_list

def is_sport_crawl():
    sport_crawl_data_origin = guardian_search("sport")

    # results 에서 원하는 부분 추출 + key 값 이름 변경
    sport_result_list = []

    for search_crawl_context in sport_crawl_data_origin:
        sport_result_dict = {}
        sport_result_dict["article_public_Date"] = search_crawl_context["webPublicationDate"]
        sport_result_dict['title'] = search_crawl_context["webTitle"]
        sport_result_dict['content_url'] = search_crawl_context["webUrl"]
        sport_result_dict['content'] = search_crawl_context["fields"]["bodyText"]
        sport_result_dict["category_id"] = 5  # 카테고리는 번호로 부여
        sport_result_list.append(sport_result_dict)

    return sport_result_list

def is_lifeandstyle_crawl():
    lifeandstyle_crawl_data_origin = guardian_search("lifeandstyle")

    # results 에서 원하는 부분 추출 + key 값 이름 변경
    lifeandstyle_result_list = []

    for search_crawl_context in lifeandstyle_crawl_data_origin:
        lifeandstyle_result_dict = {}
        lifeandstyle_result_dict["article_public_Date"] = search_crawl_context["webPublicationDate"]
        lifeandstyle_result_dict['title'] = search_crawl_context["webTitle"]
        lifeandstyle_result_dict['content_url'] = search_crawl_context["webUrl"]
        lifeandstyle_result_dict['content'] = search_crawl_context["fields"]["bodyText"]
        lifeandstyle_result_dict["category_id"] = 6  # 카테고리는 번호로 부여
        lifeandstyle_result_list.append(lifeandstyle_result_dict)

    return lifeandstyle_result_list




# 각 카테고리 별 적용해야 할 요약 딥러닝 모델 적용
# world, tech, business, environment : Berstsum 모델 적용
# sport, lifeandstyle : T5 모델 적용

def is_summarize_world(ti):
    task_instance = ti.xcom_pull(task_ids = "world_crawl")
    world_summary_list = []
    summarizer = Summarizer()

    for item in task_instance:
        body_text = item["content"]
        summary = summarizer(body_text, min_length=200, max_length=400)
        world_summary_list.append(summary)

    print(world_summary_list)
    return world_summary_list

def is_summarize_technology(ti):
    task_instance = ti.xcom_pull(task_ids = "technology_crawl")
    technology_summary_list = []
    summarizer = Summarizer()

    for item in task_instance:
        body_text = item["content"]
        summary = summarizer(body_text, min_length=200, max_length=400)
        technology_summary_list.append(summary)

    print(technology_summary_list)
    return technology_summary_list


def is_summarize_business(ti):
    task_instance = ti.xcom_pull(task_ids = "business_crawl")
    business_summary_list = []
    summarizer = Summarizer()

    for item in task_instance:
        body_text = item["content"]
        summary = summarizer(body_text, min_length=200, max_length=400)
        business_summary_list.append(summary)

    print(business_summary_list)
    return business_summary_list

def is_summarize_environment(ti):
    task_instance = ti.xcom_pull(task_ids = "environment_crawl")
    environment_summary_list = []
    summarizer = Summarizer()

    for item in task_instance:
        body_text = item["content"]
        summary = summarizer(body_text, min_length=200, max_length=400)
        environment_summary_list.append(summary)

    print(environment_summary_list)
    return environment_summary_list

def is_summarize_sport(ti):
    task_instance = ti.xcom_pull(task_ids="sport_crawl")
    sport_news_list = task_instance

    tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
    model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
    
    sport_summary_list = []
    
    for item in sport_news_list:
        body_text = item['content']
        input_ids = tokenizer.encode(body_text, return_tensors="pt", add_special_tokens=True)
        generated_ids = model.generate(input_ids=input_ids, num_beams=2, max_length=150,  repetition_penalty=2.5, length_penalty=1.0, early_stopping=True)
        summary = tokenizer.decode(generated_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

        summary_remove_n = summary.rstrip("n")
        sport_summary_list.append(summary_remove_n)
    
    print(sport_summary_list)
    return sport_summary_list

def is_summarize_lifeandstyle(ti):
    task_instance = ti.xcom_pull(task_ids="lifeandstyle_crawl")
    environment_news_list = task_instance

    tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
    model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
    
    environment_summary_list = []
    
    for item in environment_news_list:
        body_text = item['content']
        input_ids = tokenizer.encode(body_text, return_tensors="pt", add_special_tokens=True)
        generated_ids = model.generate(input_ids=input_ids, num_beams=2, max_length=150,  repetition_penalty=2.5, length_penalty=1.0, early_stopping=True)
        summary = tokenizer.decode(generated_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

        summary_remove_n = summary.rstrip("n")
        environment_summary_list.append(summary_remove_n)
    
    print(environment_summary_list)
    return environment_summary_list



# 요약 열 추가
def is_add_abstract_world(ti):
    task_instance = ti.xcom_pull(task_ids=['world_crawl', 'summarize_world'])
    news_list = task_instance[0]
    summary_list = task_instance[1]

    for i, item in enumerate(news_list):
        # 요약본 추출
        summary = summary_list[i]

        # abstract 열 추가 및 요약본 저장
        item['abstract'] = summary

    return news_list

def is_add_abstract_technology(ti):
    task_instance = ti.xcom_pull(task_ids=['technology_crawl', 'summarize_technology'])
    news_list = task_instance[0]
    summary_list = task_instance[1]

    for i, item in enumerate(news_list):
        # 요약본 추출
        summary = summary_list[i]

        # abstract 열 추가 및 요약본 저장
        item['abstract'] = summary
    
    return news_list


def is_add_abstract_business(ti):
    task_instance = ti.xcom_pull(task_ids=['business_crawl', 'summarize_business'])
    news_list = task_instance[0]
    summary_list = task_instance[1]

    for i, item in enumerate(news_list):
        # 요약본 추출
        summary = summary_list[i]

        # abstract 열 추가 및 요약본 저장
        item['abstract'] = summary
    
    return news_list


def is_add_abstract_environment(ti):
    task_instance = ti.xcom_pull(task_ids=['environment_crawl', 'summarize_environment'])
    news_list = task_instance[0]
    summary_list = task_instance[1]

    for i, item in enumerate(news_list):
        # 요약본 추출
        summary = summary_list[i]

        # abstract 열 추가 및 요약본 저장
        item['abstract'] = summary
    
    return news_list


def is_add_abstract_sport(ti):
    task_instance = ti.xcom_pull(task_ids=['sport_crawl', 'summarize_sport'])
    news_list = task_instance[0]
    summary_list = task_instance[1]

    for i, item in enumerate(news_list):
        # 요약본 추출
        summary = summary_list[i]

        # abstract 열 추가 및 요약본 저장
        item['abstract'] = summary
    
    return news_list


def is_add_abstract_lifeandstyle(ti):
    task_instance = ti.xcom_pull(task_ids=['lifeandstyle_crawl', 'summarize_lifeandstyle'])
    news_list = task_instance[0]
    summary_list = task_instance[1]

    for i, item in enumerate(news_list):
        # 요약본 추출
        summary = summary_list[i]

        # abstract 열 추가 및 요약본 저장
        item['abstract'] = summary
    
    return news_list





# MySQL에 데이터 저장하는 task
def is_store(ti):
    world_list = ti.xcom_pull(task_ids="add_abstract_world")
    technology_list = ti.xcom_pull(task_ids="add_abstract_technology")
    business_list = ti.xcom_pull(task_ids="add_abstract_business")
    environment_list = ti.xcom_pull(task_ids="add_abstract_environment")
    sport_list = ti.xcom_pull(task_ids="add_abstract_sport")
    lifeandstyle_list = ti.xcom_pull(task_ids="add_abstract_lifeandstyle")


    # 사용하려는 데이터 베이스 커넥션 정보 작성
    sql_alchemy_conn = "mysql://<username>:<password>@ec2-54-249-233-132.ap-northeast-1.compute.amazonaws.com:3306/django_dataset?charset=utf8mb4"
    

    # query 작성
    # truncate_query = """
    #         TRUNCATE TABLE home_new_article_tb;
    #     """
    
    insert_sql_query = """
            INSERT INTO home_article (article_public_Date, title, content_url, content, category_id, abstract)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
    
    delete_blank_abstract_sql_query = """
            DELETE FROM home_article WHERE abstract=''
        """

    # sqlalchemy 엔진 만들기
    engine = create_engine(sql_alchemy_conn)

    with engine.connect() as conn:
        # truncate table
        # conn.execute(truncate_query)

        # insert query
        for task_instance in [world_list, technology_list, business_list, environment_list, sport_list, lifeandstyle_list ]:
            records = task_instance
            for record in records:
                existing_article = conn.execute("SELECT * FROM home_article WHERE content_url = %s", (record['content_url'],)).fetchone()
                if not existing_article:
                    # 새로운 기사 저장
                    conn.execute(insert_sql_query, (
                        record['article_public_Date'],
                        record['title'],
                        record['content_url'],
                        record['content'],
                        record['category_id'],
                        record['abstract']
                    ))

        # delete abstract="" query
        conn.execute(delete_blank_abstract_sql_query)

def telegram():
    sql_alchemy_conn = "mysql://<username>:<password>@ec2-54-249-233-132.ap-northeast-1.compute.amazonaws.com:3306/django_dataset?charset=utf8mb4"
    engine = create_engine(sql_alchemy_conn)

    query = """
            SELECT title, abstract
            FROM home_article
            ORDER BY article_public_Date DESC
            LIMIT 6
            """
    df = pd.read_sql(query, engine)

    message = ""
    for index, row in df.iterrows():
        message += f"<b>{row['title']}</b>\n{row['abstract']}\n\n"

    message += f"더 많은 정보가 궁금하다면! <a href='54.249.233.132:8000/home'>KSC.com</a>"

    URL = 'https://api.telegram.org/<bottocken>/sendMessage?chat_id=<botid>&text='

    requests.get(URL + message + '&parse_mode=HTML')



with DAG(
    dag_id="all_crawler_test",
    schedule_interval="0 9,23 * * *",
    default_args=default_args,
    tags=["guardian", "api", "pipeline"],
    catchup=False,
) as dag:
    
    # raw 데이터 크롤링 태스크
    world_crawl = PythonOperator(task_id = "world_crawl", python_callable=is_world_crawl)
    technology_crawl = PythonOperator(task_id = "technology_crawl", python_callable=is_technology_crawl)
    business_crawl = PythonOperator(task_id = "business_crawl", python_callable=is_business_crawl)
    environment_crawl = PythonOperator(task_id = "environment_crawl", python_callable=is_environment_crawl)
    sport_crawl = PythonOperator(task_id = "sport_crawl", python_callable=is_sport_crawl)
    lifeandstyle_crawl = PythonOperator(task_id = "lifeandstyle_crawl", python_callable=is_lifeandstyle_crawl)

    # 딥러닝 적용 태스크
    summarize_world = PythonOperator(task_id = "summarize_world", python_callable=is_summarize_world)
    summarize_technology = PythonOperator(task_id = "summarize_technology", python_callable=is_summarize_technology)
    summarize_business = PythonOperator(task_id = "summarize_business", python_callable=is_summarize_business)
    summarize_environment = PythonOperator(task_id = "summarize_environment", python_callable=is_summarize_environment)
    summarize_sport = PythonOperator(task_id = "summarize_sport", python_callable=is_summarize_sport)
    summarize_lifeandstyle = PythonOperator(task_id = "summarize_lifeandstyle", python_callable=is_summarize_lifeandstyle)

    # 요약문 붙이는 태스크
    add_abstract_world = PythonOperator(task_id = "add_abstract_world", python_callable=is_add_abstract_world)
    add_abstract_technology = PythonOperator(task_id = "add_abstract_technology", python_callable=is_add_abstract_technology)
    add_abstract_business = PythonOperator(task_id = "add_abstract_business", python_callable=is_add_abstract_business)
    add_abstract_environment = PythonOperator(task_id = "add_abstract_environment", python_callable=is_add_abstract_environment)
    add_abstract_sport = PythonOperator(task_id = "add_abstract_sport", python_callable=is_add_abstract_sport)
    add_abstract_lifeandstyle = PythonOperator(task_id = "add_abstract_lifeandstyle", python_callable=is_add_abstract_lifeandstyle)

    # mysql 에 넣는 태스크
    store = PythonOperator(task_id="store", python_callable=is_store)

    # 텔레그램에 보내는 테스크
    telegram_message = PythonOperator(task_id='telegram_message', python_callable=telegram)


    world_crawl >> summarize_world >> add_abstract_world >> store >> telegram_message
    technology_crawl >> summarize_technology >> add_abstract_technology >> store >> telegram_message
    business_crawl >> summarize_business >> add_abstract_business >> store >> telegram_message
    environment_crawl >> summarize_environment >> add_abstract_environment >> store >> telegram_message
    sport_crawl >> summarize_sport >> add_abstract_sport >> store >> telegram_message
    lifeandstyle_crawl >> summarize_lifeandstyle >> add_abstract_lifeandstyle >> store >> telegram_message