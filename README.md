# User Management App

Веб-приложение для управления пользователями на Flask.

## Функции

- Аутентификация пользователей
- Админ-панель для управления пользователями (CRUD)
- Разграничение прав доступа (admin/user)

## Требования

- Python 3.x
- Flask
- SQLite

## Установка

```bash
pip install flask
```

## Запуск

```bash
python app.py
```

Откройте `http://127.0.0.1:5000` в браузере.

## Структура проекту

- `app.py` — основное приложение (Flask)
- `database.py` — создание и инициализация БД SQLite
- `templates/` — HTML-шаблоны (Jinja2)
- `users.db` — база данных SQLite
- `.gitignore` — файлы для игнорирования Git

## Маршруты

- `/login` — вход
- `/dashboard` — главная страница
- `/users` — список пользователей (только admin)
- `/users/new` — создать пользователя (только admin)
- `/users/edit/<id>` — редактировать (только admin)
- `/users/delete/<id>` — удалить (только admin)
- `/logout` — выход

## Шаблоны

- `templates/login.html` — страница входа
- `templates/dashboard.html` — главная страница
- `templates/users.html` — управление пользователями

## Инициализация БД

```bash
python database.py
```

## Тестовые пользователи

- Логин: `admin`, Пароль: `admin123` (роль: admin)
- Логин: `user`, Пароль: `user123` (роль: user)

## Дополнительные файлы

- `.gitignore` — файлы для игнорирования Git
- `git-github-guide.html` — руководство по Git и GitHub
- `random_file.txt`, `random.txt` — служебные файлы