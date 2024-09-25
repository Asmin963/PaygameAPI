# PaygameAPI
Небольшая библиотека для упрощенного пользоваения маркетплейсом PayGame

# Примеры использования

## Получение информации об аккаунте

```python
from PaygameAPI import Account

token = "тут ваш refreshToken"
acc = Account(token)

print(f"Мой ник - {acc.me.username}")
print(f"Баланс - {acc.me.balance}")
print(f'Продажи - {acc.me.sales}')
```

## Автоответ на сообщение
```python
from PaygameAPI.common.events import NewMessageEvent
from PaygameAPI.common import enums
from PaygameAPI import Account, web_socket

token = "тут ваш refreshToken"
acc = Account(token)

def new_message(event: NewMessageEvent):
    # если эвент - не новое сообщение, ничего не делаем
    if event.event_type != enums.EventTypes.NEW_MESSAGE.value:
        return
    print(f"Новое сообщение в диалоге {event.message.chat_id}: {event.message.text}")
    # отправляем ответное сообщение
    acc.send_msg(event.message.chat_id, "Привет!")
    # выводим ник пользователя
    print(f"Ник пользователя - {event.message.sender.username}")

EVENT_HANDLERS = [new_message] # список функций-обработчиков событий

socket = web_socket.Socket(token, EVENT_HANDLERS) # инициализируем веб-сокет

socket.run_websocket()
```

## Заключение
Проект незавершён, немало методов не реализовано. Обновления не планируются

