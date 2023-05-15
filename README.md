# Сервис для предсказания исходов больных COVID и перенесших коронарное шунтирование

------------

## Требования

- Python 3.11.0 или выше
- MongoDB
- Docker

## Установка

Установка необходимых бибиотек
```bash
Cardio-ML-Service> python -m pip install -r .\requirements.txt
```
Приложение конфигурируется через переменные среды, прописанные в файле `.env.sample`. Необходимо создать файл `.env` и указать в нем значения переменных среды по образцу `.env.sample`. Данные переменные так же будут использованы при разворачивании контейнеров docker.

## Запуск

```bash
Cardio-ML-Service> python .\main.py
```

## Swagger
Обратившись к `http://host:port/`, можно просмотреть swagger.

## Docker
Создание контейнеров
```bash
Cardio-ML-Service> docker-compose build
```
Запуск контейнеров
```bash
Cardio-ML-Service> docker-compose up -d
```
