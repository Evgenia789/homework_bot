import logging
import os
import sys
import time

import requests
import telegram
from dotenv import load_dotenv

import exceptions
import myconstants

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

logger = logging.getLogger()
streamHandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s -  %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    logger.info(f'Сообщение: {message}. Oтправлено')
    return bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(
            myconstants.ENDPOINT,
            headers=HEADERS,
            params=params
        )
        if homework_statuses.status_code // 100 != 2:
            logger.error(
                f'Ошибка: неожиданный ответ {homework_statuses}.'
            )
            raise exceptions.UnexpectedResponseException(
                f'Ошибка: неожиданный ответ {homework_statuses}.'
            )
        return homework_statuses.json()
    except requests.exceptions.RequestException as e:
        logger.error(
            'Сбой в работе программы: ',
            f'Эндпоинт {myconstants.ENDPOINT} недоступен.'
        )
        raise ("Error: {}".format(e))


def check_response(response):
    """Проверяет ответ API на корректность."""
    result = response['homeworks']
    if result is None:
        logger.error('Отсутствует ожидаемый ключ')
        raise KeyError('Ключ "homeworks" не найден')
    if type(result) != list:
        raise TypeError('"result" не список')
    return result


def parse_status(homework):
    """Извлекает статус домашней работы."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    verdict = myconstants.HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения."""
    variable_availability = True
    for arg in [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]:
        try:
            variable_availability = variable_availability and arg
            if not variable_availability:
                logger.critical(
                    'Отсутствует обязательная переменная окружения.'
                )
        except exceptions.MissingRequiredVariableException:
            raise exceptions.MissingRequiredVariableException(
                'Отсутствует обязательная переменная окружения.'
            )
    return variable_availability


def main():
    """Основная логика работы бота."""
    check_tokens()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    status_old = ''
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            if homework:
                status = parse_status(homework[0])
                if status_old != status:
                    send_message(bot, status)
                status_old = status
            current_timestamp = response.get('current_date')
            time.sleep(myconstants.RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            print(message)
            time.sleep(myconstants.RETRY_TIME)


if __name__ == '__main__':
    main()
