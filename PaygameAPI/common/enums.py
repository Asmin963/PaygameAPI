from enum import Enum
from typing import Dict, Any


class EventTypes(Enum):
    """
    Класс описывающий типы событий
    """
    CLIENT_CONNECTION = "client_connection"
    NEW_MESSAGE = "receive"
    CHAT_READ = "dialog_read"
    ORDER_STATE = "order_state"
    NEW_ORDER = "new_order"
    NOTIFICATION = "notification"

    @staticmethod
    def get_type_name(message: Dict[str, Any]) -> 'EventTypes':
        result = message.get("result", {})
        data_content = result.get("data", {}).get("data", {})
        event_type = data_content.get("type", "")

        if "client" in result:
            return EventTypes.CLIENT_CONNECTION
        elif event_type == "order_state" and data_content.get("state") == "paid":
            return EventTypes.NEW_ORDER
        elif event_type == "receive":
            return EventTypes.NEW_MESSAGE
        elif event_type == "dialog_read":
            return EventTypes.CHAT_READ
        elif event_type == "order_state":
            return EventTypes.ORDER_STATE
        elif event_type == "notification":
            return EventTypes.NOTIFICATION
        else:
            return "unknown"


class ORDER_STATES(Enum):
    """
    Класс описывающий состояния заказов
    """
    CREATED = 1
    """Новый заказ"""
    PAID = 2
    """Заказ оплачен"""
    COMPLETED = 3
    """Заказ выполнен"""
    IN_WORK = 4
    """Заказ в работе"""
    CANCELED = 5
    """Заказ отменен"""

    @classmethod
    def from_str(cls, state_str: str):
        state_map = {
            "created": cls.CREATED,
            "paid": cls.PAID,
            "completed": cls.COMPLETED,
            "in_work": cls.IN_WORK,
            "canceled": cls.CANCELED,
        }
        return state_map.get(state_str.lower(), None)

    @property
    def description(self):
        descriptions = {
            self.CREATED: "Новый заказ",
            self.PAID: "Заказ оплачен",
            self.COMPLETED: "Заказ выполнен",
            self.IN_WORK: "Заказ в работе",
            self.CANCELED: "Заказ отменен"
        }
        return descriptions[self]

    @classmethod
    def state_name(cls, state_value):
        states = {
            1: "created",
            2: "paid",
            3: "completed",
            4: "in_work",
            5: "canceled"
        }
        return states.get(state_value, "unknown")

    def __str__(self):
        return self.state_name(self.value)


class NotificationTypes:
    """
    Класс описывающий типы уведомлений
    """
    NEW_ORDER = "order_new"
    """Новый заказ"""
    ORDER_STATE_PAID = "order_state_paid"
    """Вы оплатили заказ"""
    ORDER_STATE_COMPLETED = "order_state_completed"
    """Заказ выполнен"""
    ORDER_STATE_CANCELED = "order_state_canceled"
    """Заказ отменен"""
    ORDER_REVIEW = "order_review"
    """Новый отзыв по заказу"""
    LOT_FROZEN = "offer_frozen"
    """Товар закончился"""


