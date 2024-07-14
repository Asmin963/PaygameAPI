from typing import List, Dict, Optional, Any
from datetime import datetime
from PaygameAPI.types import Message, UserProfile, OrderHistory, Notification, BannedStatus
from PaygameAPI.common.enums import ORDER_STATES
from PaygameAPI.common import converters
from PaygameAPI.common.enums import EventTypes

class BaseEvent:
    """
    Базовое событие.

    :param channel: Канал события.
    :type channel: :obj:`str`

    :param event_type: Тип события.
    :type event_type: :obj:`str`

    :param event_id: ID события.
    :type event_id: :obj:`int`

    :param items: Дополнительные данные события.
    :type items: Optional[:obj:`Dict[str, Any]`]
    """

    def __init__(self, channel: str, event_type: str, event_id: int, items: Optional[Dict] = None):
        self.channel = channel
        self.event_type = event_type
        self.event_id = event_id
        self.items = items or {}

    @classmethod
    def from_json(cls, data: Dict[str, any]) -> 'BaseEvent':
        result = data.get("result", {})
        channel = result.get("channel", "")
        data_content = result.get("data", {}).get("data", {})
        event_type = data_content.get("type", "")
        items = data_content.get("items", {})
        event_id = items.get("id", 0)
        return cls(channel, event_type, event_id, items)


class NewMessageEvent(BaseEvent):
    """
    Событие при получении нового сообщения.

    :param message: Новое сообщение.
    :type message: :obj:`Message`

    :param dialogs_unreaded: Непрочитанные диалоги.
    :type dialogs_unreaded: :obj:`List[int]`
    """

    def __init__(self, channel: str, event_type: str, event_id: int, message: Message, dialogs_unreaded: List[int]):
        super().__init__(channel, event_type, event_id,
                         items={"message": message, "dialogs_unreaded": dialogs_unreaded})
        self.message = message
        self.dialogs_unreaded = dialogs_unreaded

    @classmethod
    def from_json(cls, data: Dict[str, any]) -> 'NewMessageEvent':
        result = data.get("result", {})
        channel = result.get("channel", "")
        data_content = result.get("data", {}).get("data", {})
        event_type = data_content.get("type", "")
        items = data_content.get("items", {})
        event_id = items.get("id", 0)

        sender_data = items.get("sender", {})
        banned = sender_data.get("banned")
        sender = UserProfile(
            username=sender_data.get("username", ""),
            avatar=sender_data.get("avatar"),
            id=sender_data.get("id", 0),
            is_active=sender_data.get("is_active", False),
            is_support=sender_data.get("is_support", False),
            banned=BannedStatus(banned.get("freeze", False), banned.get("ban", False))
        )
        message = Message(
            id=items.get("id", 0),
            sender=sender,
            created_date=items.get("created_date", ""),
            text=items.get("text", "").encode('unicode_escape').decode('unicode_escape'),
            chat_id=items.get("peer", 0),
            extra=items.get("extra"),
            media=[converters.parse_image(m) for m in items.get("media", [])],
            type=items.get("type", ""),
            service_type=items.get("service_type", ""),
            removed=items.get("removed", False),
            distrust=items.get("distrust")
        )
        dialogs_unreaded = items.get("dialogs_unreaded", [])

        return cls(channel, event_type, event_id, message, dialogs_unreaded)


class ChatReadEvent(BaseEvent):
    """
    Событие при прочтении диалога.

    :param conversation_id: ID диалога.
    :type conversation_id: :obj:`int`

    :param read_message_id: ID прочитанного сообщения.
    :type read_message_id: :obj:`int`
    """

    def __init__(self, channel: str, event_type: str, event_id: int, conversation_id: int, read_message_id: int):
        super().__init__(channel, event_type, event_id,
                         items={"conversation_id": conversation_id, "read_message_id": read_message_id})
        self.conversation_id = conversation_id
        self.read_message_id = read_message_id

    @classmethod
    def from_json(cls, data: Dict[str, any]) -> 'ChatReadEvent':
        result = data.get("result", {})
        channel = result.get("channel", "")
        data_content = result.get("data", {}).get("data", {})
        event_type = data_content.get("type", "")
        items = data_content.get("items", {})
        conversation_id = items.get("conversation_id", 0)
        read_message_id = items.get("id", 0)

        return cls(channel, event_type, read_message_id, conversation_id, read_message_id)


class OrderStateChangeEvent(BaseEvent):
    """
    Событие при изменении статуса заказа. (type == "order_state")

    :param state: Новый статус заказа.
    :type state: :obj:`str`

    :param order_id: ID заказа.
    :type order_id: :obj:`str`

    :param history: История заказа.
    :type history: :obj:`OrderHistory`

    :param purchases: Количество покупок.
    :type purchases: :obj:`int`

    :param sales: Количество продаж.
    :type sales: :obj:`int`
    """

    def __init__(self, channel: str, event_type: str, event_id: int, state: str, order_id: str, history: OrderHistory,
                 purchases: int, sales: int):
        super().__init__(channel, event_type, event_id, items={
            "state": state,
            "order_id": order_id,
            "history": history,
            "orders": {
                "purchases": purchases,
                "sales": sales
            }
        })
        self.state = ORDER_STATES.from_str(state)
        self.order_id = order_id
        self.history = history
        self.purchases = purchases
        self.sales = sales

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'OrderStateChangeEvent':
        result = data.get("result", {})
        channel = result.get("channel", "")
        data_content = result.get("data", {}).get("data", {})
        event_type = data_content.get("type", "")
        state = data_content.get("state", "")
        order_id = data_content.get("order_id", "")
        history_data = data_content.get("history", {})
        history = OrderHistory(
            id=history_data.get("id", 0),
            state=history_data.get("state", ""),
            created_date=datetime.fromisoformat(history_data.get("created_date", ""))
        )
        orders = data_content.get("orders", {})
        purchases = orders.get("purchases", 0)
        sales = orders.get("sales", 0)

        return cls(channel, event_type, history.id, state, order_id, history, purchases, sales)


class NotificationEvent(BaseEvent):
    """
    Событие при получении новой уведомки.

    :param notification: Новое уведомление.
    :type notification: :obj:`Notification`

    :param notices: Количество непрочитанных уведомлений.
    :type notices: :obj:`int`
    """

    def __init__(self, channel: str, event_type: str, event_id: int, notification: Notification, notices: int):
        super().__init__(channel, event_type, event_id, items={
            "notification": notification,
            "notices": notices
        })
        self.notification = notification
        self.notices = notices

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'NotificationEvent':
        result = data.get("result", {})
        channel = result.get("channel", "")
        data_content = result.get("data", {}).get("data", {})
        event_type = data_content.get("type", "")
        notification_data = data_content.get("data", {})
        notification = Notification(
            is_read=notification_data.get("is_read", False),
            created_date=datetime.fromisoformat(notification_data.get("created_date", "")),
            uuid_id=notification_data.get("uuid_id", ""),
            verb=notification_data.get("verb", ""),
            content_id=notification_data.get("content_id", ""),
            title=notification_data.get("title", None),
            date_of_reading=notification_data.get("date_of_reading", None),
            meta=notification_data.get("meta", "")
        )
        notices = data_content.get("notices", 0)

        return cls(channel, event_type, notification.uuid_id, notification, notices)


class ClientConnectionEvent(BaseEvent):
    """
    Событие при подключении клиента к websocket.

    :param client: Идентификатор клиента.
    :type client: :obj:`str`

    :param version: Версия клиента.
    :type version: :obj:`str`

    :param expires: Срок действия истекает.
    :type expires: :obj:`bool`

    :param ttl: Время жизни в секундах.
    :type ttl: :obj:`int`

    :param subs: Подписки клиента.
    :type subs: :obj:`Dict[str, Any]`
    """

    def __init__(self, channel, event_type: str, event_id: int, client: str, version: str, expires: bool, ttl: int, subs: Dict[str, Any]):
        super().__init__(channel, event_type, event_id, items={
            "client": client,
            "version": version,
            "expires": expires,
            "ttl": ttl,
            "subs": subs
        })
        self.channel = channel
        self.client = client
        self.version = version
        self.expires = expires
        self.ttl = ttl
        self.subs = subs

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'ClientConnectionEvent':
        result = data.get("result", {})
        private_channel = next((c for c in list(result.get("subs").keys()) if "#" in c), None)
        event_type = "client_connection"
        event_id = data.get("id", 1)
        client = result.get("client", "")
        version = result.get("version", "")
        expires = result.get("expires", False)
        ttl = result.get("ttl", 0)
        subs = result.get("subs", {})

        return cls(private_channel, event_type, event_id, client, version, expires, ttl, subs)
