# producer 에서 보낸 거 consumer 에서 받는다

from kafka import KafkaConsumer

BROKER_SERVERS = ["172.31.21.53:9092"]
TOPIC_NAME = "streaming"

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=BROKER_SERVERS)

# [ producer ] -- 스트림(메시지) --> [ topic ] -- 스트림(큐) -->  [ consumer ]
#                                           토픽에 쌓여진 메시지를 컨슈머가 가져간다. 컨슈머는 (토픽에 데이터가 쌓일 때 까지)무한 대기... -> BLOCK 되고 있다. 

print("WAIT ... ")

for message in consumer:
    print(message)