# 1. Базовый образ
FROM python:3.12-slim

# 2. Установка рабочей директории внутри контейнера
WORKDIR /app

# 3. Установка системных зависимостей (если нужны)
# RUN apt-get update && apt-get install -y ...

# 4. Копирование файлов с зависимостями и установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копирование всего кода проекта в рабочую директорию
COPY . .

# 6. Команда для запуска приложения
CMD ["python", "-m", "tg_bot.start"] 