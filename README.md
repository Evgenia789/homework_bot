# homework_bot
Чат-бот Telegram для получения информации о проведенном код-ревью домашнего задания (Telegram API)
Проект размещен на Heroku.

## Стек технологий
Программа написана на Python с использованием:
- request (направление http-запроса на сервер)  
- python-dotenv (загрузка и считывание переменных окружения из файла .env)
- python-telegram-bot (работа с Телеграм-ботом)

## Описание работы программы
Чат-бот Telegram обращается к API, которое возвращает изменение статуса проверки домашнего задания и сообщает: 
- работа взята в ревью  
- ревью успешно пройдено  
- в работе есть ошибки, нужно поправить

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Evgenia789/homework_bot
``` 
```
cd homework_bot
``` 
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
``` 
```
source env/bin/activate
``` 
```
python3 -m pip install --upgrade pip
``` 
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
``` 
Создайте чат-бот Telegram

Создайте в дериктории файл .env и поместите туда необходимые токены в формате  PRACTICUM_TOKEN = 'XXXXXXXXXX', TELEGRAM_TOKEN = 'XXXXXXXXXX', TELEGRAM_CHAT_ID = 'XXXXXXXXXX'  

Откройте файл homework.py и запустите код  

## Пример ответа чат-бота Telegram:
{
   "homeworks":[
      {
         "id":123,
         "status":"approved",
         "homework_name":"username__hw_test.zip",
         "reviewer_comment":"Всё нравится",
         "date_updated":"2020-02-11T14:40:57Z",
         "lesson_name":"Тестовый проект"
      }],
   "current_date":1581604970
} 
