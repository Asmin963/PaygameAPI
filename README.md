# PaygameAPI
Небольшая библиотека для упрощенного пользоваения маркетплейсом PayGame

# Примеры использования

## Получение информации об аккаунте

```python
from PaygameAPI import Bot
from PaygameAPI.common.events import NewMessageEvent, OrderStateChangeEvent

token = "refreshToken Here"
bot = Bot(token)

print(f"Мой ник - {bot.me.username}")
print(f"Баланс - {bot.me.balance}")
print(f'Рейтинг - {bot.me.rating}')

# обработчик новых сообщений, если в тексте есть "привет"
@bot.message_handler(text_contains="привет")
def new_message(event: NewMessageEvent):
    print(f"Новое сообщение в диалоге {event.message.chat_id}: {event.message.text}")
    # отправляем ответное сообщение
    bot.send_message(event.message.chat_id, "Привет!")
    # выводим ник пользователя
    print(f"Ник пользователя - {event.message.sender.username}")

# регистрируем обработчик новых заказов
@bot.order_handler()
def new_order_handler(event: OrderStateChangeEvent):
    print(f"Обнаружен новый заказ - {event.order_id}")

# запускаем обработчик событий (websocket)
bot.start()
```

## Заключение
Проект незавершён, немало методов не реализовано. Обновления не планируются

