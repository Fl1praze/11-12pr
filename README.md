# Movie Booking System / Система бронирования фильмов

This is a movie booking system built with FastAPI and SQLAlchemy. It allows users to register, login, book movie tickets, and manage halls.

Это система бронирования фильмов, построенная с использованием FastAPI и SQLAlchemy. Она позволяет пользователям регистрироваться, входить в систему, бронировать билеты на фильмы и управлять залами.

## Features / Возможности

- User registration and authentication / Регистрация и аутентификация пользователей
- Movie management (add, update, delete) / Управление фильмами (добавление, обновление, удаление)
- Hall management / Управление залами
- Booking system with seat selection / Система бронирования с выбором мест
- Error handling and validation / Обработка ошибок и валидация


## Project Structure / Структура проекта

- `app/`: Contains the main application code / Содержит основной код приложения
  - `bookings/`: Booking-related functionality / Функциональность, связанная с бронированием
  - `halls/`: Hall management / Управление залами
  - `users/`: User authentication and management / Аутентификация и управление пользователями
  - `movie/`: Movie management / Управление фильмами
  - `dao/`: Data access objects / Объекты доступа к данным
  - `migrations/`: Database migrations / Миграции базы данных
  - `config.py`: Configuration settings / Настройки конфигурации
  - `database.py`: Database connection setup / Настройка подключения к базе данных

