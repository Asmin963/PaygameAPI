import os
from typing import List

from bs4 import BeautifulSoup as bs
from . import web_socket
from .common import apihelper, converters, exceptions, enums
from .types import API_Methods, UserProfile, Blacklist, Message, Image, ImageMeta, SelfUserProfile, Order, Notification, \
    NotificationWidget, UserReviews, GameServer, OffersGame


class Account:
    def __init__(self, token: str, requests_timeout: int | float = 10, user_agent: str = None):
        self.token_path = os.path.join(os.path.abspath(__file__), "..", "token.json")

        self.headers = {
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'connection': 'keep-alive',
            "Origin": 'https://paygame.ru',
            "Referer": 'https://paygame.ru/',
        }

        self.token = token

        self.requests_timeout = requests_timeout
        self.me = self.get_me()

        # Thread(target=self.loop_refresh_token).start()

    def _refresh_token(self) -> bool:
        self.token = apihelper._refresh_token(self.token)
        return self.token

    def get_user(self, username: str = None, user_id: int = None) -> UserProfile | SelfUserProfile:
        """
        Возвращает объект пользователя
        Должен присутствовать либо Username, либо ID (ID имеет больший вес, если переданы оба аргумента, username будет проигнорирован)

        :param username: ник пользователя
        :param user_id: идентификатор пользователя

        :return: Экземпляр UserProfile, если профиль не текущего аккаунта, иначе SelfUserProfile
        """
        user_data = apihelper.get_user_info(self.token, username, user_id)
        return converters.parse_user_profile(user_data.json())

    def get_me(self) -> SelfUserProfile:
        response = apihelper.get_me(API_Methods.base_url, self.headers, self.token)
        name_elem = bs(response.text, "html.parser").find("span", class_="sc-1qhtcg6-2 dBWgoR")
        if not name_elem:
            raise exceptions.RequestFailedError(response)
        name = name_elem.text
        return self.get_user(name)

    def online_users(self):
        response = apihelper._make_request("get", API_Methods.online_users, self.headers, token=self.token)
        return response.json()

    def create_offer(self, game_id: int, offer_type: int, price: int, quantity: int, description: str, title: str,
                     auto_delivery: list | None = None, is_active: bool = True) -> int:
        """
        Создает новый лот (предложение)

        :param game_id: int - ID игры
        :param offer_type: int - тип предложения
        :param price: int - Цена в рублях
        :param quantity: int - Количество товара
        :param description: str - Описание
        :param title: str - название
        :param auto_delivery: List[str] Список товаров в авто-выдаче
        :param is_active: bool - Активен ли лот?

        :return: ID предложения
        """
        payload = {
            "game": game_id,
            "offer_type": offer_type,
            "is_active": is_active,
            "price": price,
            "title": title,
            "description": description,
            "quantity": quantity,
            "offer_data": []
        }
        if not auto_delivery:
            payload["unlimited"] = True
        else:
            payload["unlimited"] = False
            payload["auto_delivery"] = [{
                "blurred": True, "error": None, "id": f"autoDelivery_{i}", "offer": None, "text": text
            } for i, text in enumerate(auto_delivery, start=1)]

        response = apihelper._make_request("post", API_Methods.create_offer, payload=payload,
                                           token=self.token)
        return response.json().get('id')

    def read_notifications(self):
        """
        Читает все новые уведомления

        :return:
        """
        resp = apihelper.mark_all_as_read(self.token)
        return not any(e in resp.json() for e in ["error", "errors"])

    def get_order(self, order_id: str) -> Order:
        """
        Получает заказ по айди

        :param order_id: идентификатор заказа
        :return: Экземпляр Order
        """
        response = apihelper.get_order(self.token, order_id)
        return converters.parse_order(response.json())

    def send_msg(self, chat_id: int, message: str = None, image: str = None) -> Message:
        """
        Отправляет сообщение в указанный чат (chat_id)
        Должно присутствовать сообщение или медиа

        :param chat_id: ID чата
        :param message: сообщение. Опционально
        :param image: UUID изображения для отправки. Опционально

        :return: Экземпляр Message
        """
        if not image and not message:
            raise exceptions.IncorrectRequest("Нельзя отправить пустое сообщение")
        response = apihelper.send_msg(self.token, chat_id, message, image)
        return converters.parse_message(response.json())

    def reply_to_review(self, review_id: int, text: str, edit: bool = False, return_obj: bool = False):
        """
        Отправляет ответ на отзыв

        :param review_id: ID отзыва
        :param text: текст ответа
        :param edit: True, если ответ на отзыв должен быть редактирован. False, если новый ответ
        :param return_obj: True, если нужно вернуть ответ в виде объекта отзыва. False, если нужно вернуть только ID ответа

        :return True если успешно, иначе False
        """
        resp = apihelper.reply_to_review(self.token, review_id, text, edit)
        if return_obj:
            return converters.parse_review(resp.json())
        else:
            return not any(e in resp.json() for e in ["error", "errors"])

    def upload_image(self, image: bytes) -> Image:
        """
        Выгружает изображение на сервера PayGame

        :param image: байтовые данные изображения
        :return: Экземпляр Image
        """
        response = apihelper.upload_image(self.token, image)
        if (json := response.json()).get("id"):
            return converters.parse_image(json)

    def chat_messages(self, chat_id: int, page_size: int = 25):
        """
        Получает сообщения из чата

        :param chat_id: ID чата

        :return: Экземляр Chat
        """
        response = apihelper.get_chat_messages(self.token, chat_id, page_size)
        return converters.parse_chat_messages(response.json())

    def get_chats(self):
        """
        Получает все чаты

        :return: Экземпляр ChatList
        """
        response = apihelper.get_messager(self.token)
        return converters.parse_chat_list(response.json())

    def read_messages(self, chat: int):
        """
        Читает все сообщения в чате
        :param chat: ID чата
        :return: True если успешно, иначе False
        """
        resp = apihelper.read_messages(self.token, chat)
        return not any(e in resp.json() for e in ["error", "errors"])

    def get_latest_notifications(self):
        """
        Получает последние уведомления (Виджет уведомлений)

        :return: Экземпляр NotificationWidget
        """
        response = apihelper.get_latest_notifications(self.token)
        notifications = converters.parse_notification_widget(response.json())
        return notifications

    def get_notifications(self, page_size=10, verb: enums.NotificationTypes = None, cursor: str = None):
        """
        Получает последние уведомления

        :param page_size: кол-во уведомлений на 1 странице
        :param verb: Тип уведомления (получить только определенные)
        :param cursor: курсор для получения следующей/предыдущей страницы уведомлений

        :return: Экземпляр NotificationList
        """
        response = apihelper.get_all_notifications(self.token, page_size, verb, cursor)
        return converters.parse_notification_list(response.json())

    def get_reviews(self, username: str, page: int = 1) -> UserReviews:
        """
        Получает отзывы пользователя

        :param username: Юзернейм пользователя
        :param page: Номер страницы

        :return: экзепляр UserReviews
        """
        response = apihelper.get_reviews(self.token, username, page)
        return converters.parse_rewiews(response.json())

    def change_settings(self, em_not=True, tg_ap=True, tg_not=True, brwsr_not=False, tg_wio=False) -> SelfUserProfile:
        """
        Изменение настроек уведомлений профиля

        :param em_not: уведомления на почту
        :param tg_ap: уведомления в телеграм
        :param tg_not: уведомление в телеграм, если юзер пингует
        :param brwsr_not: уведомления в барузере (тестовая функция)
        :param tg_wio: уведомление "даже когда я онлайн"

        :return: экземпляр класса SelfUserProfile
        """
        payload = {
            "em_not": em_not,
            "tg_ap": tg_ap,
            "tg_not": tg_not,
            "brwsr_not": brwsr_not,
            "tg_wio": tg_wio
        }
        response = apihelper.change_data(self.token, **payload)
        return converters.parse_user_profile(response.json())

    # незавершенные методы

    def order_in_work(self, order_id: str):
        """
        Принятие заказа в работу
        :param order_id:
        :return:
        """
        ...

    def order_refund(self, order_id: str):
        """
        Возврат средств по заказу
        :param order_id:
        :return:
        """
        ...

    def cancel_order(self, order_id: str):
        """
        Отмена заказа со стороны покупателя
        :param order_id:
        :return:
        """
        ...

    def get_games(self):
        """
        Получение списка игр со страницы paygame.ru/games
        :return:
        """
        ...

    def get_offers_from_game(self) -> OffersGame:
        """
        Получение предложений из игры
        :return:
        """
        ...

    def withdrawal(self):
        """
        Вывод средств
        :return:
        """
        ...

    def transactions(self):
        """
        Получение транзакций
        :return:
        """
        ...

    def ticket_support(self):
        """
        Отправка тикета с поддержку
        :return:
        """
        ...

    def get_faq(self):
        """
        Получение FAQ сайта
        """
        ...

    # методы не реализованы и не планируются
