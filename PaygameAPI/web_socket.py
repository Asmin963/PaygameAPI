import json
import logging
import time
from .common import events, enums
from .common.enums import EventTypes
import websocket
from typing import List, Callable, Dict, Any
from threading import Thread

logger = logging.getLogger("websocket")


class Socket:
    def __init__(self, token: str, NEW_EVENT_HANDLERS: List = None, OPEN_HANDLERS: list = None,
                 CLOSE_HANDLERS: list = None, ERROR_HANDLERS: list = None, reconnect_socket: bool = True, **kwargs):
        """
        Инициализация WebSocket клиента.

        :param token: RefreshToken от PayGame
        :type token: :obj:`str`

        :param NEW_EVENT_HANDLERS: Список обработчиков новых событий.
        :type NEW_EVENT_HANDLERS: :obj:`List[callable]`

        :param OPEN_HANDLERS: Список обработчиков после аутентификации пользователя в вебсокете.
        :type OPEN_HANDLERS: :obj:`List[callable]`

        :param CLOSE_HANDLERS: Список обработчиков закрытия соединения.
        :type CLOSE_HANDLERS: :obj:`List[callable]`

        :param ERROR_HANDLERS: Список обработчиков ошибок.
        :type ERROR_HANDLERS: :obj:`List[callable]`

        :param reconnect_socket: Переподключаться при потере соединения?
        :type reconnect_socket: :obj:`bool`
        """
        self.token = token
        self.ERROR_HANDLERS = ERROR_HANDLERS or []
        self.OPEN_HANDLERS = OPEN_HANDLERS or []
        self.CLOSE_HANDLERS = CLOSE_HANDLERS or []
        self.NEW_EVENT_HANDLERS = NEW_EVENT_HANDLERS or []

        self.reconnect_socket = reconnect_socket

        self.first_msg = False  # Флаг, устанавливается на True, после получения первого сообщения
        self.channel: str | None = None  # Приватный канал, по которому будут идти запросы

    def check_type_event(self, message: dict) -> EventTypes:
        """
        Определение типа события на основе сообщения из вебсокета.

        :param message: Сообщение в формате JSON.
        :type message: :obj:`Dict[str, Any]`

        :return: Тип события.
        :rtype: :obj:`EventTypes`
        """
        return EventTypes.get_type_name(message)

    def create_event(self, data: Dict[str, Any], event_type: EventTypes) -> events.BaseEvent:
        """
        Создание события на основе сообщения из вебсокета.

        :param data: Данные события.
        :type data: :obj:`Dict[str, Any]`

        :return: Событие.
        :rtype: :obj:`events.BaseEvent`
        """
        if event_type == EventTypes.CLIENT_CONNECTION:
            return events.ClientConnectionEvent.from_json(data)
        elif event_type == EventTypes.NEW_MESSAGE:
            return events.NewMessageEvent.from_json(data)
        elif event_type == EventTypes.CHAT_READ:
            return events.ChatReadEvent.from_json(data)
        elif event_type in (EventTypes.NEW_ORDER.value, EventTypes.ORDER_STATE.value):
            return events.OrderStateChangeEvent.from_json(data)
        elif event_type == EventTypes.NOTIFICATION:
            return events.NotificationEvent.from_json(data)
        else:
            return events.BaseEvent.from_json(data)

    def on_message(self, ws, message):
        """
        Хендлер сообщений.

        :param ws: WebSocket соединение.
        :type ws: :obj:`websocket.WebSocketApp`

        :param message: Сообщение в формате JSON.
        :type message: :obj:`dict`
        """
        msg_json = json.loads(message)
        e_type = self.check_type_event(msg_json)
        event = self.create_event(msg_json, EventTypes.get_type_name(msg_json))
        if not self.first_msg and e_type == EventTypes.CLIENT_CONNECTION:
            self.first_msg = True
            for handler in self.OPEN_HANDLERS:
                Thread(target=handler, args=(event,), daemon=True).start()
            self.channel = event.channel
            # print(f"Websocket готов принимать события")
            return
        if event.channel != self.channel:
            return
        for handler in self.NEW_EVENT_HANDLERS:
            Thread(target=handler, args=(event,), daemon=True).start()

    def on_error(self, ws, error):
        """
        Хендлер ошибкок.

        :param ws: WebSocket соединение.
        :type ws: :obj:`websocket.WebSocketApp`

        :param error: Ошибка.
        :type error: :obj:`Exception`
        """
        for handler in self.ERROR_HANDLERS:
            Thread(target=handler, args=(error,), daemon=True).start()

    def on_close(self, ws, close_status_code, close_msg):
        """
        Хендлер закрытия соединения.

        :param ws: WebSocket соединение.
        :type ws: :obj:`websocket.WebSocketApp`

        :param close_status_code: Код статуса закрытия.
        :type close_status_code: :obj:`int`

        :param close_msg: Сообщение о закрытии.
        :type close_msg: :obj:`str`
        """
        for handler in self.CLOSE_HANDLERS:
            Thread(target=handler, args=(close_status_code, close_msg), daemon=True).start()
        # print(f"Соединение закрыто: {close_status_code} - {close_msg}")
        time.sleep(5)
        if self.reconnect_socket:
            self.run_websocket()

    def on_open(self, ws):
        """
        Обработчик открытия соединения.

        :param ws: WebSocket соединение.
        :type ws: :obj:`websocket.WebSocketApp`
        """
        auth_data = {
            "params": {
                "token": self.token
            },
            "id": 1
        }
        ws.send(json.dumps(auth_data))

    def run_websocket(self, **kwargs):
        """
        Запуск WebSocket клиента.
        """
        self.ws = websocket.WebSocketApp(
            "wss://ws.paygame.ru/connection/websocket",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open,
            **kwargs
        )
        self.ws.run_forever()
