# TRON Service

## Задача
> Написать микросервис, который будет выводить информацию по адресу в сети трон, его bandwidth, energy, и баланс trx, ендпоинт должен принимать входные данные - адрес.

## Переменные окружения .env
```markdown
# Postgres Environment Variables
POSTGRES_USERNAME="postgres" # Для локального запуска - изменить
POSTGRES_PASSWORD="postgres" # Для локального запуска - изменить
POSTGRES_HOST=postgres # Для локального запуска - изменить
POSTGRES_PORT="5432"
POSTGRES_DB="tron"
```

## 🐳 Запуск проекта в Docker
```shell
docker compose -f docker-compose.yml --env-file ./src/.env up -d
```

## Запуск проекта локально
```shell
cd src
uvicorn main:app --host 127.0.0.1 --port 8080
```

## Benchmarks
...