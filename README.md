# Проект "Онлайн Кинотеатр"

## Сервис UGC +

Репозиторий для сервиса, направленного на улучшение функционала UGC. Включает в себя настройку CI/CD процессов, сравнение использования MongoDB с ClickHouse для хранения данных, настройку системы логирования с использованием Sentry и ELK для более эффективного мониторинга и отладки.

## Содержание:

- [Django Admin Panel](https://github.com/kaedeMirai/new_admin_panel_sprint_1) - **Панель администратора для управления контентом: Удобный и интуитивно понятный интерфейс для управления фильмами, сеансами и другим контентом вашего кинотеатра.**
- [ETL](https://github.com/kaedeMirai/admin_panel_sprint_3) - **Перенос данных из PostgreSQL в ElasticSearch для реализации полнотекстового поиска**
- [Auth](https://github.com/kaedeMirai/Auth_sprint_1-2) - **Аутентификация и авторизация пользователей на сайте с системой ролей**
- [UGC](https://github.com/kaedeMirai/ugc_sprint_1) - **Сервис для удобного хранения аналитической информации и UGC**
- [UGC +](https://github.com/kaedeMirai/ugc_sprint_2) - **Улучшение функционала UGC внедрением CI/CD процессов и настройкой системы логирования Setnry и ELK**
- [Notification service]() - **Отправка уведомлений пользователям о важных событиях и акциях в кинотеатре.**
- [Watch Together service]() - **Позволяет пользователям смотреть фильмы совместно в реальном времени, обеспечивая синхронизацию видео и чата.**

## Где найти код?
1. [9 sprint](https://github.com/kaedeMirai/ugc_sprint_2) - здесь хранится код заданий 9 спринта

## Ссылка на документацию api
1. http://0.0.0.0:8282/api/openapi

## Инструкция по запуску проекта
1. Склонировать репозиторий:

   ```
   git clone https://github.com/kaedeMirai/ugc_sprint_2.git
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