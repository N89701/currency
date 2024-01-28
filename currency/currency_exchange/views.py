from collections import deque
from datetime import datetime
import requests

from django.conf import settings
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit


URL = settings.CURRENCY_URL  # наш URL для получения курса доллара к рублю

REQUEST_LOG = deque(maxlen=10)  # используем Дек вместо обычного списка


# декоратор для ограничения количества запросов по времени
@ratelimit(key='ip', rate='1/10s', block=True)
def get_current_usd(request):
    response = requests.get(URL)  # делаем запрос на наш URL
    usd_rate = response.json()['rates']["RUB"]  # получаем текущий курс

    REQUEST_LOG.appendleft(  # вставляем в начало дека время запроса и курс
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rate": usd_rate
        }
    )

    data = {  # подготавливаем JSON-ответ
        "usd_rate": usd_rate,
        "request_log": list(REQUEST_LOG)
    }

    return JsonResponse(data)  # отвечаем


# в случае превышения частоты запросов возникает 403 ошибка,
#  которую мы перехватываем, отдавая данные из нашего Дека
def handler_403(request, exception):

    data = {  # достаем наш "кэш"
        "usd_rate": REQUEST_LOG[0]['rate'],
        "request_log": list(REQUEST_LOG)
    }

    return JsonResponse(data)  # отдаем
