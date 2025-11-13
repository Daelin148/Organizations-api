### Инструкция по запуску проекта ###

- Склонировать проект из репозитория
- Перейти в корень проекта
- Создать файл переменных окружения 
```
cp .env.example .env
```
- Запустить docker-compose.yml
```
docker compose -f 'docker-compose.yml' up -d --build
```

Документация доступна по адресу: /docs
Api-ключ лежит в .env.example