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
docker compose -f docker-compose.yml --env-file .env up -d
```

## Запуск проекта локально
```shell
cd src
uvicorn main:app --host 127.0.0.1 --port 8080
```

## Benchmarks
```shell
# /tests/load/
locust -f locustfile.py --host http://localhost --class
```

### POST /api/v1/accounts/{address}
![total_requests_per_second_1743522618 484](https://github.com/user-attachments/assets/281b4e40-8a6b-4502-af40-9a86908a1c61)

### GET /api/v1/requests
![total_requests_per_second_1743523168 893](https://github.com/user-attachments/assets/6a379728-8fb7-4179-abb3-47c43d26cd2b)