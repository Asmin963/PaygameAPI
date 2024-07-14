import PaygameAPI
from PaygameAPI import Account, web_socket
from PaygameAPI.common.events import NewMessageEvent
from PaygameAPI.common import enums
from pprint import pprint

token = "тут refreshToken"
acc = Account(token)

print(f"Мой ник - {acc.me.username}")
print(f"Баланс - {acc.me.balance}")
print(f'Продаж - {acc.me.sales}')

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

socket.run_websocket() # запускам сокет (ждем и обрабатываем события)
