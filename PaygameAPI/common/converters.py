from datetime import datetime

from ..types import UserNotifications, UserPlan, UserProfile, SelfUserProfile, Message, OfferData, GameServer, Image, \
    ImageMeta, Order, OrderHistory, Notification, NotificationWidget, Chat, Draft, ChatList, NotificationList, Review, \
    ReviewReply, ReviewOrder, UserReviews, Blacklist, UserBlacklist, OffersGame
from typing import Dict, List

def parse_pages(data: Dict) -> Dict:
    return {
        "current_page": data.get('current_page'),
        "next": data.get('next'),
        "last_page": data.get('last_page'),
        "previous": data.get('previous'),
        "current_page_url": data.get('current_page_url'),
        "next_url": data.get("next_url"),
        "last_page_url": data.get("last_page_url"),
        "previous_url": data.get("prev_page_url"),
        "total": data.get('total'),
        "start_index": data.get('start_index'),
        "end_index": data.get('end_index')
    }

def parse_user_profile(data: Dict) -> UserProfile | SelfUserProfile:
    """
    Преобразует JSON-объект в экземпляр UserProfile или SelfUserProfile.

    :param data: JSON-объект с данными пользователя.
    :type data: :obj:`Dict`

    :return: Экземпляр UserProfile или SelfUserProfile.
    :rtype: :obj:`UserProfile` или :obj:`SelfUserProfile`
    """
    plan_data = data.get("plan")
    plan = UserPlan(
        id=plan_data["id"],
        title=plan_data["title"],
        slug=plan_data["slug"],
        image=plan_data["image"]
    ) if plan_data else None

    notifications_data = data.get("notifications")
    notifications = UserNotifications(
        browser=notifications_data["browser"],
        telegram=notifications_data["telegram"]
    ) if notifications_data else None

    banned = data.get("banned")

    blocked_data = data.get("blocked")
    blocked_from_me = blocked_data["from_me"] if blocked_data else None
    blocked_remote = blocked_data["remote"] if blocked_data else None

    common_kwargs = {
        "username": data["username"],
        "avatar": data.get("avatar"),
        "id": data["id"],
        "is_online": data.get("is_online"),
        "is_active": data.get("is_active"),
        "last_active": datetime.fromisoformat(data["last_active"]) if data.get("last_active") else None,
        "is_support": data.get("is_support"),
        "banned": banned,
        "notifications": notifications,
        "plan": plan,
        "about": data.get("about"),
        "date_joined": datetime.fromisoformat(data["date_joined"]) if data.get("date_joined") else None,
        "rating": data.get("rating"),
        "extra": data.get("extra"),
        "is_verified": data.get("is_verified"),
        "purchases": data["purchase_sale"]["purchase"] if data.get("purchase_sale") else None,
        "sales": data["purchase_sale"]["sale"] if data.get("purchase_sale") else None,
        "review_count": data.get("review_count"),
        "blocked_from_me": blocked_from_me,
        "blocked_remote": blocked_remote,
        "lots": data.get("lots"),
        "trusted": data.get("trusted")
    }

    if "email" in data:
        return SelfUserProfile(
            email=data["email"],
            phone=data.get("phone"),
            balance=data["balance"],
            last_read=data["last_read"],
            config=data["config"],
            referral_code=data["referral_code"],
            referral_percent=data["referral_percent"],
            email_confirmed=data["email_confirmed"],
            notices=data["notices"],
            orders=data["orders"],
            raise_limits=data["raise_limits"],
            access_ideas=data["access_ideas"],
            cc_percent=data.get("cc_percent"),
            laws=data["laws"],
            **common_kwargs
        )
    else:
        return UserProfile(**common_kwargs)


def parse_message(data: Dict) -> Message:
    """
    Преобразует JSON-объект в экземпляр Message.

    :param data: JSON-объект с данными сообщения.
    :type data: :obj:`Dict`

    :return: Экземпляр Message.
    :rtype: :obj:`Message`
    """
    sender_data = data["sender"]
    sender = parse_user_profile(sender_data)

    return Message(
        id=data["id"],
        sender=sender,
        created_date=data["created_date"],
        text=data["text"],
        chat_id=data["peer"],
        extra=data.get("extra"),
        media=[parse_image(image) for image in data.get("media", [])],
        type=data["type"],
        service_type=data["service_type"],
        removed=data["removed"],
        distrust=data.get("distrust")
    )

def parse_image(data: Dict) -> Image:
    """
    Преобразует JSON-объект в экземпляр Image.

    :param data: JSON-объект с данными изображения.
    :type data: :obj:`Dict`

    :return: Экземпляр Image.
    :rtype: :obj:`Image`
    """
    return Image(
        id=data.get("id"),
        file=data.get("file", None),
        type=data.get("type", "media"),
        image=data.get("image", None),
        meta=ImageMeta(width=data["meta"]["width"], height=data["meta"]["height"]) if data.get("meta") else None,
        preview=data.get("preview"),
        completed=data.get("completed", None)
    )

def parse_game_server(data: Dict) -> GameServer:
    """
    Преобразует JSON-объект в экземпляр GameServer.

    :param data: JSON-объект с данными сервера игры.
    :type data: :obj:`Dict`

    :return: Экземпляр GameServer.
    :rtype: :obj:`GameServer`
    """
    return GameServer(
        id=data.get("id"),
        icon=data.get("icon"),
        slug=data.get("slug"),
        title=data.get("title"),
        has_servers=data.get("has_servers")
    )

def parse_offer_data(data: Dict) -> OfferData:
    """
    Преобразует JSON-объект в экземпляр OfferData.

    :param data: JSON-объект с данными пользователя.
    :type data: :obj:`Dict`

    :return: Экземпляр UserProfile или SelfUserProfile.
    :rtype: :obj:`UserProfile` или :obj:`SelfUserProfile`
    """
    seller = parse_user_profile(data.get("seller", {}))
    game = parse_game_server(data.get("game", {}))
    images = [parse_image(image) for image in data.get("media", [])]

    return OfferData(
        id=data.get("id"),
        game=game,
        item=data.get("item"),
        pack=data.get("pack"),
        price=str(data.get("price")),
        risks=data.get("risks", []),
        title=data.get("title"),
        views=data.get("views", {}),
        images=images,
        seller=seller,
        category=data.get("category"),
        quantity=str(data.get("quantity")),
        is_active=data.get("is_active"),
        is_frozen=data.get("is_frozen"),
        unlimited=data.get("unlimited"),
        offer_data=data.get("props_data", []),
        offer_type=data.get("offer_type"),
        video_link=data.get("video_link", ""),
        description=data.get("description", ""),
        game_server=data.get("game_server", []),
        last_raised=datetime.fromisoformat(data.get("last_raised")) if data.get("last_raised") else None,
        created_date=datetime.fromisoformat(data.get("created_date")) if data.get("created_date") else None,
        auto_delivery=data.get("auto_delivery", False),
        minimal_quantity=str(data.get("minimal_quantity", ""))
    )

def parse_order_history(data: List[Dict]) -> List[OrderHistory]:
    """
    Преобразует JSON-объекты в экземпляры OrderHistory.

    :param data: JSON-объекты с данными истории заказов.
    :type data: :obj:`List[Dict]`

    :return: Экземпляры OrderHistory.
    :rtype: :obj:`List[OrderHistory]`
    """
    return [
        OrderHistory(
            id=item.get("id"),
            state=item.get("state"),
            created_date=datetime.fromisoformat(item.get("created_date"))
        )
        for item in data
    ]

def parse_order(data: Dict) -> 'Order':
    """
    Преобразует JSON-объект в экземпляр Order.

    :param data: JSON-объект с данными заказа.
    :type data: :obj:`Dict`

    :return: Экземпляр Order.
    :rtype: :obj:`Order`
    """
    customer = parse_user_profile(data.get("customer", {}))
    seller = parse_user_profile(data.get("seller", {}))
    offer_data = parse_offer_data(data.get("offer_data", {}))
    offer = parse_offer_data(data.get("offer", {}))
    order_history = parse_order_history(data.get("order_history", []))

    return Order(
        order_id=data.get("order_id"),
        customer=customer,
        quantity=data.get("quantity"),
        amount=data.get("amount"),
        seller=seller,
        nickname=data.get("nickname"),
        state=data.get("state"),
        created_date=datetime.fromisoformat(data.get("created_date")),
        offer_data=offer_data,
        reviewed=data.get("reviewed", False),
        offer=offer,
        order_history=order_history,
        transaction=data.get("transaction"),
        funds_requested=data.get("funds_requested", False),
        deadline=datetime.fromisoformat(data.get("deadline")) if data.get("deadline") else None,
        auto_delivery=data.get("auto_delivery", []),
        options=data.get("options", [])
    )


def parse_notification(data: Dict) -> Notification:
    return Notification(
        is_read=data.get("is_read"),
        created_date=datetime.fromisoformat(data.get("created_date")),
        uuid_id=data.get("uuid_id"),
        verb=data.get("verb"),
        content_id=data.get("content_id"),
        title=data.get("title"),
        date_of_reading=datetime.fromisoformat(data.get("date_of_reading")) if data.get("date_of_reading") else None,
        meta=data.get("meta")
    )

def parse_notification_widget(data: Dict) -> NotificationWidget:
    results = [parse_notification(notification) for notification in data.get("results", [])]

    return NotificationWidget(
        next=data.get("next"),
        previous=data.get("previous"),
        next_cursor=data.get("next_cursor"),
        previous_cursor=data.get("previous_cursor"),
        results=results
    )

def parse_chat_list(data: Dict) -> ChatList:
    """
    Преобразует JSON-объект в экземпляр ChatList.

    :param data: JSON-объект с данными списка чатов.
    :type data: :obj:`Dict`

    :return: Экземпляр ChatList.
    :rtype: :obj:`ChatList`
    """
    chat_results = []
    for chat in data.get('results', []):
        users = [parse_user_profile(user) for user in chat.get('users', [])]
        last_message = parse_message(chat.get('last_message'))
        draft_data = chat.get('draft')
        draft = Draft(text=draft_data['text'], has_media=draft_data['has_media']) if draft_data else None

        chat_obj = Chat(
            id=chat.get('id'),
            uid=chat.get('uid'),
            count=chat.get('count'),
            users=users,
            last_message=last_message,
            draft=draft,
            last_read=chat.get('last_read'),
            date_pin=chat.get('date_pin'),
            pins=chat.get('pins')
        )
        chat_results.append(chat_obj)

    return ChatList(
        count=data.get('count'),
        next=data.get('next'),
        previous=data.get('previous'),
        results=chat_results
    )

def parse_chat_messages(data: Dict) -> Chat:
    """
    Преобразует JSON-объект в экземпляр Chat.

    :param data: JSON-объект с данными чата.
    :type data: :obj:`Dict`

    :return: Экземпляр Chat.
    :rtype: :obj:`Chat`
    """
    users = [parse_user_profile(user) for user in data.get('users', [])]
    messages = [parse_message(message) for message in data.get('data', {}).get('results', [])]
    draft_data = data.get('draft')
    draft = Draft(text=draft_data['text'], has_media=draft_data['has_media']) if draft_data else None

    chat_obj = Chat(
        id=data.get('id'),
        uid=data.get('id'),
        count=data.get('count'),
        users=users,
        last_message=messages[-1] if messages else None,
        draft=draft,
        last_read=data.get('last_read'),
        date_pin=data.get("date_pin"),
        pins=data.get('pins')
    )

    return chat_obj

def parse_notification_list(data: Dict[str, str]) -> NotificationList:
    """
    Преобразует JSON-объекты в экземпляр NotificationList.

    :param data: JSON-объекты с данными списка уведомлений.
    :type data: :obj:`Dict`

    :return: Экземпляр NotificationList
    """
    results = [parse_notification(notification) for notification in data.get('results', [])]

    return NotificationList(
        next=data.get('next'),
        previous=data.get('previous'),
        next_cursor=data.get('next_cursor'),
        previous_cursor=data.get('previous_cursor'),

        results=results
    )


def parse_review(data: Dict) -> Review:
    """
    Преобразует JSON-объект в экземпляр Review.

    :param data: JSON-объект с данными обзора.
    :type data: :obj:`Dict`

    :return: Экземпляр Review.
    """
    seller = parse_user_profile(data["recipient"])

    author = parse_user_profile(data["author"])

    reply = ReviewReply(
        text=data['reply']['text'],
        date=datetime.fromisoformat(data['reply']['date'])
    ) if data.get('reply') else None

    order = ReviewOrder(
        id=data['order']['id'],
        state=data['order']['state'],
        amount=data['order']['amount'],
        offer=data['order']['offer']
    )

    return Review(
        id=data['id'],
        seller=seller,
        author=author,
        rating=data['rating'],
        text=data['text'],
        reply=reply,
        order=order,
        created_date=datetime.fromisoformat(data['created_date']),
        is_anonymous=data['is_anonymous'],
        is_included_in_rating=data['is_included_in_rating']
    )

def parse_rewiews(data: Dict) -> UserReviews:
    """
    Преобразует JSON-объекты в экземпляр UserReviews.

    :param data: JSON-объекты с данными отзывов.
    :type data: :obj:`Dict`

    :return: Экземпляр UserReviews.
    """
    reviews = [parse_review(review) for review in data.get('results', [])]
    kwargs = parse_pages(data)
    return UserReviews(results=reviews, **kwargs)

def parse_blacklist(data: Dict) -> Blacklist:
    """
    Преобразует JSON-объекты в экземпляр Blacklist.

    :param data: JSON-объекты с данными черного списка.
    :type data: :obj:`Dict`

    :return: Экземпляр Blacklist.
    """
    results = [parse_user_profile(u) for u in data.get("results", [])]
    kwargs = parse_pages(data)
    return Blacklist(results=results, **kwargs)

def parse_offers_from_game(data: Dict) -> OffersGame:
    """
    Преобразует JSON-объекты в экземпляр OffersGame.

    :param data: JSON-объекты с данными предложений в игре.
    :type data: :obj:`Dict`

    :return: Экземпляр OffersGame.
    """
    offers = [parse_offer_data(offer) for offer in data.get("results", [])]
    kwargs = parse_pages(data)
    return OffersGame(results=offers, **kwargs)


