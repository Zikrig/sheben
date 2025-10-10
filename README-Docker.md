# Docker Setup для Telegram Bot

Этот проект настроен для работы в Docker контейнерах с PostgreSQL базой данных.

## Быстрый старт

### 1. Настройка переменных окружения

Скопируйте файл `env.example` в `.env` и заполните необходимые значения:

```bash
cp env.example .env
```

Отредактируйте `.env` файл:
```env
# Database configuration
DB_USER=postgres
DB_PASSWORD=your_secure_password_here
DB_HOST=postgres
DB_NAME=sheben_db

# Telegram Bot Token
TOKEN=your_bot_token_here
```

### 2. Запуск проекта

Запустите все сервисы с помощью docker-compose:

```bash
docker-compose up -d
```

### 3. Просмотр логов

Для просмотра логов бота:
```bash
docker-compose logs -f bot
```

Для просмотра логов базы данных:
```bash
docker-compose logs -f postgres
```

## Управление контейнерами

### Остановка сервисов
```bash
docker-compose down
```

### Перезапуск бота
```bash
docker-compose restart bot
```

### Пересборка образа
```bash
docker-compose build --no-cache bot
```

### Подключение к базе данных
```bash
docker-compose exec postgres psql -U postgres -d sheben_db
```

## Структура проекта

- `Dockerfile` - конфигурация для сборки образа бота
- `docker-compose.yml` - оркестрация сервисов (бот + PostgreSQL)
- `.dockerignore` - файлы, исключаемые из Docker контекста
- `data/` - директория для файлов бота (монтируется как volume)
- `logs/` - директория для логов

## Полезные команды

### Очистка Docker
```bash
# Удалить неиспользуемые образы
docker image prune

# Удалить все неиспользуемые ресурсы
docker system prune -a
```

### Бэкап базы данных
```bash
docker-compose exec postgres pg_dump -U postgres sheben_db > backup.sql
```

### Восстановление базы данных
```bash
docker-compose exec -T postgres psql -U postgres sheben_db < backup.sql
```

## Troubleshooting

### Проблемы с подключением к базе данных
1. Убедитесь, что PostgreSQL контейнер запущен: `docker-compose ps`
2. Проверьте логи PostgreSQL: `docker-compose logs postgres`
3. Убедитесь, что в `.env` файле `DB_HOST=postgres`

### Проблемы с правами доступа к файлам
```bash
# Создайте директории с правильными правами
mkdir -p data logs
chmod 755 data logs
```

### Проблемы с памятью
Если контейнеры падают из-за нехватки памяти, увеличьте лимиты в `docker-compose.yml`:

```yaml
services:
  bot:
    # ... другие настройки
    deploy:
      resources:
        limits:
          memory: 512M
```
