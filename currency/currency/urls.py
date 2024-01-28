from django.urls import path
from currency_exchange.views import get_current_usd

urlpatterns = [
    path('get-current-usd/', get_current_usd),
]

handler403 = 'currency_exchange.views.handler_403'
