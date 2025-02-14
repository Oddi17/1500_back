from fastapi import Request
from fastapi.responses import JSONResponse
import logging
from logging.handlers import RotatingFileHandler
import time
import os

# # Создание папки для логов, если её нет
# log_dir = "C:/allin/projectsProg/1500/logs"
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)

# Настройка ротации логов
# log_file = os.path.join(log_dir, "app.log")
log_handler = RotatingFileHandler("app.log", maxBytes=1000000, backupCount=2)  # maxBytes=1MB

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        log_handler,  # Запись логов в файл
        logging.StreamHandler()  # Также выводим логи в консоль
    ]
)

logger = logging.getLogger()

async def log_requests(request: Request, call_next):
    start_time = time.time()
    # Получаем тело запроса
    body = await request.body()
    body_content = body.decode("utf-8") if body else "EMPTY_BODY"
    query_params = request.query_params if request.query_params else "EMPTY_QUERY"
     # Обработка запроса
    response = await call_next(request)
    process_time = time.time() - start_time
    # Логируем запрос
    if request.method == "GET":
        logging.info(f"Request - {request.method} {request.url} - Process Time: {process_time:.2f} сек")
    elif request.method == "POST":
        if "login" in body_content:
            body_array = body_content.strip("{}").split(",")
            login_str = body_array[0]
            logging.info(f"Request - {request.method} {request.url} - Request Body: {login_str}- Process Time: {process_time:.2f} сек")
        else:
            logging.info(f"Request - {request.method} {request.url} - Request Body: {body_content[:20]} - Process Time: {process_time:.2f} сек")
    else:
        logging.info(f"Request - {request.method} {request.url} - Process Time: {process_time:.2f} сек")
    # Логируем ответ
    if isinstance(response, JSONResponse):
        # response_body = response.body.decode("utf-8")
        response_body = b"".join([chunk async for chunk in response.body_iterator]).decode("utf-8")
        # Логируем ошибки (если статус код 4xx или 5xx)
        if 400 <= response.status_code < 600:
            logging.error(f"Error Response Status: {response.status_code} | Response Body: {response_body[:30]}")
        else:
            # Логируем успешные ответы
            logging.info(f"Response Status: {response.status_code} | Response Body: {response_body[:30]}")
    else:
        # Для других типов ответов (например, текстовых)
        logging.info(f"Response Status: {response.status_code}")
        # Логируем ошибки для других типов ответов
        if 400 <= response.status_code < 600:
            logging.error(f"Error Response Status: {response.status_code}")
    return response