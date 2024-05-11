# producer

from kafka import KafkaProducer
import datetime
import pytz
import time
import random
import json
from faker import Faker
fake = Faker()

# 브로커 목록을 정의
#  - 브로커가 한 개만 있어도 리스트 형식으로 조회
#  - 여러 개의 브로커가 띄어진 상태에서도 한 개의 브로커만 입력하는 것이 아닌, 모든 브로커의 목록을 입력


BROKER_SERVERS=["172.31.21.53"] # AWS 프라입시 IPV4 주소를 넣기
TOPIC_NAME = "streaming"


def generate_fake_data():
    age = random.randint(14, 59) # 10살 단위로 끊어서 
    if 14 <= age <= 19:
        occupation = random.choices(['student', 'worker', 'job_seeker', 'etc'], weights=[0.9, 0.05, 0.03, 0.02])[0]
        signup_purpose = random.choices(['language improvement', 'overseas investment', 'interest', 'etc'], weights=[0.5, 0.1, 0.3, 0.1])[0]
        article_category = random.choices(['Technology', 'Sports', 'Business', 'World', 'lifestyle', 'Environment'], weights=[0.1, 0.3, 0.1, 0.1, 0.1, 0.3])[0]
        click_day = random.choices(['Sun', 'Mon', 'Tus', 'Wed', 'Tue', 'Fri', 'Sat'], weights=[0.05, 0.1, 0.2, 0.2, 0.2, 0.2, 0.05 ])[0]
        click_time = random.choices(list(range(1, 25)), weights=[1 if (7 <= i <= 9) or (18 <= i <= 24) else 0.1 for i in range(1, 25)])[0]

    elif 20 <= age <= 29:
        occupation = random.choices(['student', 'worker', 'job_seeker', 'etc'], weights=[0.6, 0.2, 0.15, 0.05])[0]
        signup_purpose = random.choices(['language improvement', 'overseas investment', 'interest', 'etc'], weights=[0.5, 0.2, 0.2, 0.1])[0]
        article_category = random.choices(['Technology', 'Sports', 'Business', 'World', 'lifestyle', 'Environment'], weights=[0.2, 0.1, 0.1, 0.1, 0.45, 0.05])[0]
        click_day = random.choices(['Sun', 'Mon', 'Tus', 'Wed', 'Tue', 'Fri', 'Sat'], weights=[0.05, 0.1, 0.2, 0.2, 0.2, 0.2, 0.05 ])[0]
        click_time = random.choices(list(range(1, 25)), weights=[1 if (8 <= i <= 10) or (18 <= i <= 24) else 0.1 for i in range(1, 25)])[0]

    elif 30 <= age <39:
        occupation = random.choices(['student', 'worker', 'job_seeker', 'etc'], weights=[0.05, 0.8, 0.2, 0.05])[0]
        signup_purpose = random.choices(['language improvement', 'overseas investment', 'interest', 'etc'], weights=[0.3, 0.5, 0.1, 0.1])[0]
        article_category = random.choices(['Technology', 'Sports', 'Business', 'World', 'lifestyle', 'Environment'], weights=[0.3, 0.2, 0.3, 0.1, 0.05, 0.05])[0]
        click_day = random.choices(['Sun', 'Mon', 'Tus', 'Wed', 'Tue', 'Fri', 'Sat'], weights=[0.05, 0.1, 0.2, 0.2, 0.2, 0.2, 0.05 ])[0]
        click_time = random.choices(list(range(1, 25)), weights=[1 if (6 <= i <= 10) or (17 <= i <= 20) else 0.1 for i in range(1, 25)])[0]

    elif 40 <= age <49:
        occupation = random.choices(['student', 'worker', 'job_seeker', 'etc'], weights=[0.05, 0.8, 0.1, 0.05])[0]
        signup_purpose = random.choices(['language improvement', 'overseas investment', 'interest', 'etc'], weights=[0.3, 0.6, 0.05, 0.05])[0]
        article_category = random.choices(['Technology', 'Sports', 'Business', 'World', 'lifestyle', 'Environment'], weights=[0.1, 0.1, 0.3, 0.3, 0.1, 0.1])[0]
        click_day = random.choices(['Sun', 'Mon', 'Tus', 'Wed', 'Tue', 'Fri', 'Sat'], weights=[0.05, 0.1, 0.2, 0.2, 0.2, 0.2, 0.05 ])[0]
        click_time = random.choices(list(range(1, 25)), weights=[1 if (6 <= i <= 10) or (17 <= i <= 20) else 0.1 for i in range(1, 25)])[0]

    else:
        occupation = random.choices(['student', 'worker', 'job_seeker', 'etc'], weights=[0.01, 0.7, 0.1, 0.19])[0]
        signup_purpose = random.choices(['language improvement', 'overseas investment', 'interest', 'etc'], weights=[0.1, 0.5, 0.35, 0.05])[0]
        article_category = random.choices(['Technology', 'Sports', 'Business', 'World', 'lifestyle', 'Environment'], weights=[0.05, 0.05, 0.3, 0.2, 0.1, 0.4])[0]
        click_day = random.choices(['Sun', 'Mon', 'Tus', 'Wed', 'Tue', 'Fri', 'Sat'], weights=[0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.1 ])[0]
        click_time = random.choices(list(range(1, 25)), weights=[1 if (6 <= i <= 8) or (17 <= i <= 21) else 0.1 for i in range(1, 25)])[0]

    return age, occupation, signup_purpose, article_category, click_day, click_time

    

if __name__ == "__main__":
    
    producer = KafkaProducer(bootstrap_servers=BROKER_SERVERS)
    
    # 데이터 발생 및 스트리밍
    while True:
        
        # 랜덤하게 만들어진 결제 정보 얻기
        age, occupation, signup_purpose, article_category, click_day, click_time = generate_fake_data()
        
        # 스트리밍할 데이터 조립
        row_data = {
            "age": age,
            "occupation": occupation,
            "signup_purpose": signup_purpose,
            "article_category": article_category,
            "click_day" : click_day,
            "click_time" : int(click_time),
        }
        
        # 바이너리화 해서 데이터를 토픽에 전송
        producer.send(TOPIC_NAME, json.dumps(row_data).encode("utf-8"))
        producer.flush()
        
        print(row_data)
        time.sleep(1)