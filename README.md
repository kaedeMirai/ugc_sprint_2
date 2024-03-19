# Проектная работа 8 спринта

## Где найти код?
1. [9 sprint](https://github.com/Munewxar/ugc_sprint_2) - здесь хранится код заданий 9 спринта

## Ссылка на документацию api
1. http://0.0.0.0:8282/api/openapi

## Инструкция по запуску проекта
1. Склонировать репозиторий:

   ```
   git clone https://github.com/Munewxar/ugc_sprint_2.git
   ```
2. Скопировать .env.example в .env (либо переименовать .env.example) и заполнить их
3. В командной строке запустить проект:

    ```
    make build
    make run
    ```
4. Для настройки кластера mongo необходимо прописать следующие команды:
    ```
    docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
    docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
    docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh' 
    docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
    docker exec -it mongors1n1 bash -c 'echo "use activities" | mongosh'
    docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"activities\")" | mongosh'
    docker exec -it mongos1 bash -c 'echo "db.createCollection(\"activities.user-activities\")" | mongosh'
    docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"activities.user-activities\", {\"user_id\": \"hashed\"})" | mongosh'
   ```
   
5. Для запуска тестов необходимо выполнить следующую команду:
   ```
   make run_tests
   ```