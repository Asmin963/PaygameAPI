from datetime import datetime
from typing import List, Optional, Dict


class API_Methods:
    base_url = 'https://paygame.ru'
    url_v1 = 'https://api.paygame.ru/api/v1/'
    url = 'https://paygame.com/api'
    profile = url_v1 + '/profile'
    signin = url + '/sign-in'
    signout = url + '/sign-out'
    online_users = profile + '/online-users'
    token = url + '/token'
    refresh = 'https://paygame.ru/api/token/refresh'
    news_last = 'https://api.paygame.ru/api/v1/news/last/'

    games_list = 'https://api.paygame.ru/api/v1/games/list/'
    games_detail = 'https://api.paygame.ru/api/v1/games/detail/'

    user_info = 'https://api.paygame.ru/api/v1/profile/user/'  # params: username
    create_offer = 'https://api.paygame.ru/api/v1/offers/create-offer/'
    support = 'https://api.paygame.ru/api/v1/support/'
    user_data = 'https://api.paygame.ru/api/v1/user/user-data/'
    seller_in_work = 'https://api.paygame.ru/api/v1/orders/{}/seller-in-work/'

    change_data = 'https://api.paygame.ru/api/v1/profile/change-data/'
    change_password = 'https://api.paygame.ru/api/v1/user/password/change-password/'
    blacklist = 'https://api.paygame.ru/api/v1/black-list/'  # params: page: int
    coupon_add = 'https://api.paygame.ru/api/v1/coupons/add/'

    latest_notifications = 'https://api.paygame.ru/api/v1/notifications/latest-notifications/'
    read_notifications = 'https://api.paygame.ru/api/v1/notifications/mark-all-as-read/'
    notifications = 'https://api.paygame.ru/api/v1/notifications/'  # params: page_size: int

    messanger_detail = 'https://api.paygame.ru/api/v1/messager/detail'
    messanger_add = 'https://api.paygame.ru/api/v1/messager/{}/add/'  # format: dialog
    messanger = 'https://api.paygame.ru/api/v1/messager/'
    messanger_read = 'https://api.paygame.ru/api/v1/messager/{}/read/'  # format: dialog
    messanger_ping = 'https://api.paygame.ru/api/v1/messager/ping/{}/'


class Params:
    # Идентификаторы для уведомлений
    order_state_canceled = 1
    order_new = 2
    """Новый заказ"""
    order_state_paid = 3
    """Вы оплатили заказ"""
    order_state_completed = 4

    offer_frozen = 5
    """Заказ оплачен"""
    order_review = 6
    """Новый отзыв"""

    # Идентификаторы для поддержки
    agency_contract = 1
    other = 2
    complaint = 3
    license_agreement = 4
    transfer_offers = 5
    transfer_rating = 6
    verification = 7
    offering_type = 8
    account = 9
    order = 10
    pay = 11
    site = 12
    collab = 13

    def __init__(self):
        self.dict_params_support = {
            'agency-contract': 'Агентский договор',
            'other': 'Другое',
            'complaint': 'Жалоба на пользователя',
            'license-agreement': 'Лицензионное соглашение',
            'transfer-offers': 'Перенос объявлений с другой площадки',
            'transfer-rating': 'Перенос рейтинга с другой площадки',
            'verification': 'Подтверждение личности',
            'offering-type': 'Предложить раздел',
            'account': 'Проблема с аккаунтом',
            'order': 'Проблема с заказом',
            'pay': 'Проблема с оплатой',
            'site': 'Проблема с сайтом',
            'collab': 'Сотрудничество'
        }

        self.dict_params_notifications = {
            "order_new": "Новый заказ",
            "order_state_paid": "Вы оплатили заказ",
            "order_state_completed": "Сделка завершена",
            "order_state_canceled": "Заказ отменен",
            "offer_frozen": "Лот закончился",
            "order_review": "Отзыв"
        }

        self.dict_params_support_reverse = {v: k for k, v in self.dict_params_support.items()}
        self.dict_params_notifications_reverse = {v: k for k, v in self.dict_params_notifications.items()}

        self.support_ids = {
            self.agency_contract: 'agency-contract',
            self.other: 'other',
            self.complaint: 'complaint',
            self.license_agreement: 'license-agreement',
            self.transfer_offers: 'transfer-offers',
            self.transfer_rating: 'transfer-rating',
            self.verification: 'verification',
            self.offering_type: 'offering-type',
            self.account: 'account',
            self.order: 'order',
            self.pay: 'pay',
            self.site: 'site',
            self.collab: 'collab'
        }

        self.notification_ids = {
            self.order_state_canceled: "order_state_canceled",
            self.order_new: "order_new",
            self.order_state_paid: "order_state_paid",
            self.order_state_completed: "order_state_completed",
            self.offer_frozen: "offer_frozen",
            self.order_review: "order_review"
        }


class BasePages:
    """
    Базовый класс для объектов со страницами (Черный список, отзывы и т. д.)

    :param current_page: Номер текущей страницы
    :type current_page: :obj:`int`

    :param next: Номер следующей страницы
    :type next: :obj:`int`

    :param last_page: Номер последней страницы
    :type last_page: :obj:`int`

    :param previous: Номер предыдущей страницы
    :type previous: :obj:`int`

    :param current_page_url: URL текущей страницы
    :type current_page_url: :obj:`str`

    :param next_url: URL следующей страницы
    :type next_url: :obj:`str`

    :param last_page_url: URL последней страницы
    :type last_page_url: :obj:`str`

    :param previous_url: URL предыдущей страницы
    :type previous_url: :obj:`str`

    :param total: Всего результатов
    :type total: :obj:`int`

    :param start_index: Номер первого результата на текущей странице
    :type start_index: :obj:`int`

    :param end_index: Номер последнего результата на текущей странице
    :type end_index: :obj:`int`

    :param results: Результаты текущей страницы
    :type results: :obj:`list`
    """
    def __init__(self, current_page: int = None, next: int = None, last_page: int = None, previous: int = None,
                 current_page_url: str = None, next_url: str = None,
                 last_page_url: str = None, previous_url: str = None, total: int = None, start_index: int = None,
                 end_index: int = None, results: list = None):
        self.current_page = current_page
        self.next = next
        self.last_page = last_page
        self.previous = previous
        self.current_page_url = current_page_url
        self.next_url = next_url
        self.last_page_url = last_page_url
        self.previous_url = previous_url
        self.total = total
        self.start_index = start_index
        self.end_index = end_index
        self.results = results



class ImageMeta:
    """
    Класс для представления метаданных изображения.

    :param width: Ширина изображения
    :type width: :obj:`int`

    :param height: Высота изображения
    :type height: :obj:`int`
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

class BannedStatus:
    """
    Класс для представления статуса бана и заморозки.

    :param ban: Статус и причина бана
    :type ban: :obj:`dict`

    :param freeze: Статус и причина заморозки
    :type freeze: :obj:`dict`
    """
    def __init__(self, freeze: dict, ban: dict):
        self.ban_status = ban.get("status")
        self.ban_reason = ban.get("reason")
        self.freeze_status = freeze.get("status")
        self.freeze_reason = freeze.get("reason")


class Image:
    """
    Класс для представления изображения.

    :param id: ID изображения
    :type id: :obj:`int`

    :param image: URL изображения
    :type image: :obj:`str`

    :param meta: Метаданные изображения
    :type meta: :obj:`ImageMeta`

    :param completed: Завершено ли изображение
    :type completed: :obj:`bool`
    """
    def __init__(self, id: str, type: str, image: str, meta: ImageMeta, preview: dict, completed: bool, file: str = None):
        self.id = id
        self.type = type
        self.file = file
        self.image = image
        self.meta = meta
        self.url_small = preview.get("small", None)
        self.url_thumbnail = preview.get("thumbnail", None)
        self.url_orig_size = preview.get("orig_size", None)
        self.completed = completed

class UserNotifications:
    """
    Класс для представления настроек уведомлений пользователя.

    :param browser: Уведомления браузера
    :type browser: :obj:`bool`

    :param telegram: Уведомления Telegram
    :type telegram: :obj:`bool`
    """
    def __init__(self, browser: bool, telegram: bool):
        self.browser = browser
        self.telegram = telegram

class UserPlan:
    """
    Класс для представления плана пользователя.

    :param id: ID плана
    :type id: :obj:`int`

    :param title: Название плана
    :type title: :obj:`str`

    :param slug: Слаг плана
    :type slug: :obj:`str`

    :param image: Изображение плана
    :type image: :obj:`Optional[str]`
    """
    def __init__(self, id: int, title: str, slug: str, image: Optional[str]):
        self.id = id
        self.title = title
        self.slug = slug
        self.image = image

class UserProfile:
    """
    Класс для представления пользователя.

    :param username: Имя пользователя
    :type username: :obj:`str`

    :param avatar: Аватар пользователя
    :type avatar: :obj:`Optional[str]`

    :param id: ID пользователя
    :type id: :obj:`int`

    :param is_online: В сети ли пользователь
    :type is_online: :obj:`Optional[bool]`

    :param is_active: Активен ли пользователь
    :type is_active: :obj:`Optional[bool]`

    :param last_active: Дата последнего входа в систему
    :type last_active: :obj:`Optional[datetime]`

    :param is_support: Является ли пользователь поддержкой
    :type is_support: :obj:`Optional[bool]`

    :param banned: Статус блокировки и заморозки аккаунта аккаунта
    :type banned: :obj:`BannedStatus`

    :param notifications: Настройки уведомлений пользователя
    :type notifications: :obj:`Optional[UserNotifications]`

    :param plan: План пользователя
    :type plan: :obj:`Optional[UserPlan]`

    :param about: Описание пользователя
    :type about: :obj:`Optional[str]`

    :param date_joined: Дата регистрации
    :type date_joined: :obj:`Optional[datetime]`

    :param rating: Рейтинг пользователя
    :type rating: :obj:`Optional[float]`

    :param extra: Дополнительные данные
    :type extra: :obj:`Optional[Dict]`

    :param is_verified: Верифицирован ли пользователь
    :type is_verified: :obj:`Optional[bool]`

    :param purchases: Количество покупок
    :type purchases: :obj:`int`

    :param sales: Количество продаж
    :type sales: :obj:`int`

    :param review_count: Количество отзывов
    :type review_count: :obj:`Optional[int]`

    :param blocked_from_me: Заблокирован мной
    :type blocked_from_me: :obj:`bool`

    :param blocked_remote: Заблокировал меня
    :type blocked_remote: :obj:`Optional[bool]`

    :param lots: Количество лотов
    :type lots: :obj:`Optional[int]`

    :param trusted: Доверенный пользователь
    :type trusted: :obj:`Optional[bool]`
    """
    def __init__(self, username: str, avatar: Optional[str], id: int, is_online: bool = None, is_active: bool = None,
                 last_active: datetime = None, is_support: bool = None, banned: BannedStatus = None,
                 notifications: UserNotifications = None, plan: UserPlan = None, about: str = None, date_joined: datetime = None,
                 rating: float = None, extra: Dict = None, is_verified: bool = None,
                 purchases: int = None, sales: int = None, review_count: int = None, blocked_from_me: bool = None, blocked_remote: bool = None,
                 lots: int = None, trusted: bool = None):
        self.username = username
        self.avatar = avatar
        self.id = id
        self.is_online = is_online
        self.is_active = is_active
        self.last_active = last_active
        self.is_support = is_support
        self.banned = banned
        self.notifications = notifications
        self.plan = plan
        self.about = about
        self.date_joined = date_joined
        self.rating = rating
        self.extra = extra
        self.is_verified = is_verified
        self.purchases = purchases
        self.sales = sales
        self.review_count = review_count
        self.blocked_from_me = blocked_from_me
        self.blocked_remote = blocked_remote
        self.lots = lots
        self.trusted = trusted

class SelfUserProfile(UserProfile):
    """
    Класс для представления собственного профиля пользователя с дополнительной информацией.

    :param email: Email пользователя
    :type email: :obj:`str`

    :param phone: Телефон пользователя
    :type phone: :obj:`Optional[str]`

    :param balance: Баланс пользователя в рублях
    :type balance: :obj:`float`

    :param last_read: Последнее прочитанное сообщение
    :type last_read: :obj:`int`

    :param config: Конфигурационные настройки
    :type config: :obj:`Dict`

    :param referral_code: Реферальный код
    :type referral_code: :obj:`str`

    :param referral_percent: Процент рефералов
    :type referral_percent: :obj:`str`

    :param email_confirmed: Подтвержден ли email
    :type email_confirmed: :obj:`bool`

    :param notices: Количество уведомлений
    :type notices: :obj:`int`

    :param orders: Заказы пользователя
    :type orders: :obj:`Dict`

    :param raise_limits: Лимиты повышения
    :type raise_limits: :obj:`Dict`

    :param access_ideas: Имеет ли доступ к идеям
    :type access_ideas: :obj:`bool`

    :param cc_percent: Процент CC
    :type cc_percent: :obj:`Optional[str]`

    :param laws: Юридическая информация
    :type laws: :obj:`Dict`
    """
    def __init__(self, email: str, phone: Optional[str], balance: float, last_read: int, config: Dict, referral_code: str, referral_percent: str,
                 email_confirmed: bool, notices: int, orders: Dict, raise_limits: Dict, access_ideas: bool, cc_percent: Optional[str], laws: Dict, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.phone = phone
        self.balance = balance
        self.last_read = last_read
        self.config = config
        self.referral_code = referral_code
        self.referral_percent = referral_percent
        self.email_confirmed = email_confirmed
        self.notices = notices
        self.orders = orders
        self.raise_limits = raise_limits
        self.access_ideas = access_ideas
        self.cc_percent = cc_percent
        self.laws = laws

class Message:
    """
    Класс для представления последнего сообщения в чате.

    :param id: ID сообщения
    :type id: :obj:`int`

    :param sender: Отправитель сообщения
    :type sender: :obj:`User`

    :param created_date: Дата создания сообщения
    :type created_date: :obj:`str`

    :param text: Текст сообщения
    :type text: :obj:`str`

    :param chat_id: ID чата
    :type chat_id: :obj:`int`

    :param extra: Дополнительная информация
    :type extra: :obj:`Optional[Dict]`

    :param media: Медиа вложения
    :type media: :obj:`List[Dict]`

    :param type: Тип сообщения
    :type type: :obj:`str`

    :param service_type: Тип сервиса сообщения
    :type service_type: :obj:`str`

    :param removed: Было ли сообщение удалено
    :type removed: :obj:`bool`

    :param distrust: Недоверие к сообщению
    :type distrust: :obj:`Optional[Dict]`
    """
    def __init__(self, id: int, sender: UserProfile, created_date: str, text: str, chat_id: int,
                 extra: Optional[Dict], media: List[Image], type: str, service_type: str,
                 removed: bool, distrust: Optional[Dict]):
        self.id = id
        self.sender = sender
        self.created_date = created_date
        self.text = text
        self.chat_id = chat_id
        self.extra = extra
        self.media = media
        self.type = type
        self.service_type = service_type
        self.removed = removed
        self.distrust = distrust

    def __str__(self):
        return self.text

class Draft:
    """
    Класс для представления черновика сообщения.

    :param text: Текст черновика
    :type text: :obj:`str`

    :param has_media: Наличие медиа
    :type has_media: :obj:`int`
    """
    def __init__(self, text: str, has_media: int):
        self.text = text
        self.has_media = has_media

class Chat:
    """
    Класс для представления чата.

    :param id: ID чата
    :type id: :obj:`int`

    :param uid: UID чата
    :type uid: :obj:`str`

    :param count: Количество сообщений
    :type count: :obj:`int`

    :param users: Участники чата
    :type users: :obj:`List[User]`

    :param last_message: Последнее сообщение в чате
    :type last_message: :obj:`LastMessage`

    :param draft: Черновик сообщения
    :type draft: :obj:`Optional[Draft]`

    :param last_read: Последнее прочитанное сообщение
    :type last_read: :obj:`int`

    :param date_pin: Дата закрепления
    :type date_pin: :obj:`str`

    :param pins: Закрепления
    :type pins: :obj:`list`


    """
    def __init__(self, id: int, count: int, users: List[UserProfile], uid: str = None, last_message: Message = None,
                 draft: Optional[Draft] = None, last_read: int = None, date_pin: str = None, pins: list = None):
        self.id = id
        self.uid = uid
        self.count = count
        self.users = users
        self.last_message = last_message
        self.draft = draft
        self.last_read = last_read
        self.date_pin = date_pin
        self.pins = pins

class ChatList:
    """
    Класс для представления списка чатов.

    :param count: Количество чатов
    :type count: :obj:`int`

    :param next: Следующая страница
    :type next: :obj:`Optional[str]`

    :param previous: Предыдущая страница
    :type previous: :obj:`Optional[str]`

    :param results: Список чатов
    :type results: :obj:`List[Chat]`
    """
    def __init__(self, count: int, next: Optional[str], previous: Optional[str], results: List[Chat]):
        self.count = count
        self.next = next
        self.previous = previous
        self.results = results

class Blacklist(BasePages):
    """
    Класс для представления черного списка.

    :param results: Список черных пользователей
    :type results: :obj:`List[Blacklist]`
    """
    def __init__(self, results: List[UserProfile], **kwargs):
        super().__init__(results=results, **kwargs)


class UserBlacklist:
    """
    Класс для представления черного списка пользователей.

    :param id: ID записи черного списка
    :type id: :obj:`int`

    :param user: Пользователь
    :type user: :obj:`User`

    :param created_date: Дата создания записи
    :type created_date: :obj:`datetime`
    """
    def __init__(self, id: int, user: UserProfile, created_date: datetime):
        self.id = id
        self.user = user
        self.created_date = created_date

class GameServer:
    """
    Класс для представления сервера игры.

    :param id: ID сервера
    :type id: :obj:`int`

    :param icon: URL иконки сервера
    :type icon: :obj:`Optional[str]`

    :param slug: Слаг сервера
    :type slug: :obj:`str`

    :param title: Название сервера
    :type title: :obj:`str`

    :param has_servers: Имеет ли серверы
    :type has_servers: :obj:`bool`
    """
    def __init__(self, id: int, icon: Optional[str], slug: str, title: str, has_servers: bool):
        self.id = id
        self.icon = icon
        self.slug = slug
        self.title = title
        self.has_servers = has_servers

    def __str__(self):
        return self.title

class OfferType:
    """
    Класс для представления типа предложения.

    :param id: ID типа
    :type id: :obj:`int`

    :param slug: Строка-идентификатор типа
    :type slug: :obj:`str`

    :param name: Название типа
    :type name: :obj:`str`

    :param position: Положение в списке
    :type position: :obj:`str`

    :param variant: Вариант предложения. Опционально
    :type variant: :obj:`str`
    """
    def __init__(self, id: int, slug: str, name: str, position: str, variant: str = "default"):
        self.id = id
        self.slug = slug
        self.name = name
        self.position = position
        self.variant = variant

class OfferData:
    """
    Класс для представления данных предложения.

    :param id: ID предложения
    :type id: :obj:`int`

    :param game: Информация о сервере игры
    :type game: :obj:`GameServer`

    :param item: Предмет предложения
    :type item: :obj:`Optional[Dict]`

    :param pack: Пакет предложения
    :type pack: :obj:`int`

    :param price: Цена предложения
    :type price: :obj:`str`

    :param risks: Риски предложения
    :type risks: :obj:`List`

    :param title: Заголовок предложения
    :type title: :obj:`str`

    :param views: Просмотры предложения
    :type views: :obj:`Dict[str, int]`

    :param images: Изображения предложения
    :type images: :obj:`List[Image]`

    :param seller: Продавец предложения
    :type seller: :obj:`UserProfile`

    :param category: Категория предложения
    :type category: :obj:`Optional[Dict]`

    :param quantity: Количество предложения
    :type quantity: :obj:`str`

    :param is_active: Активно ли предложение
    :type is_active: :obj:`bool`

    :param is_frozen: Заморожено ли предложение
    :type is_frozen: :obj:`bool`

    :param unlimited: Неограниченное предложение
    :type unlimited: :obj:`bool`

    :param offer_data: Данные предложения
    :type offer_data: :obj:`List[Dict]`

    :param offer_type: Тип предложения
    :type offer_type: :obj:`OfferType`

    :param video_link: Ссылка на видео
    :type video_link: :obj:`str`

    :param description: Описание предложения
    :type description: :obj:`str`

    :param game_server: Сервер игры
    :type game_server: :obj:`List[Dict]`

    :param last_raised: Дата последнего поднятия
    :type last_raised: :obj:`datetime`

    :param created_date: Дата создания предложения
    :type created_date: :obj:`datetime`

    :param auto_delivery: Автоматическая доставка
    :type auto_delivery: :obj:`bool`

    :param minimal_quantity: Минимальное количество
    :type minimal_quantity: :obj:`str`
    """
    def __init__(self, id: int, game: GameServer, item: Optional[Dict], pack: int, price: str, risks: List,
                 title: str, views: Dict[str, int], images: List[Image], seller: UserProfile, category: Optional[Dict],
                 quantity: str, is_active: bool, is_frozen: bool, unlimited: bool, offer_data: List[Dict],
                 offer_type: OfferType, video_link: str, description: str, game_server: List[Dict], last_raised: datetime,
                 created_date: datetime, auto_delivery: bool, minimal_quantity: str):
        self.id = id
        self.game = game
        self.item = item
        self.pack = pack
        self.price = price
        self.risks = risks
        self.title = title
        self.views = views
        self.images = images
        self.seller = seller
        self.category = category
        self.quantity = quantity
        self.is_active = is_active
        self.is_frozen = is_frozen
        self.unlimited = unlimited
        self.offer_data = offer_data
        self.offer_type = offer_type
        self.video_link = video_link
        self.description = description
        self.game_server = game_server
        self.last_raised = last_raised
        self.created_date = created_date
        self.auto_delivery = auto_delivery
        self.minimal_quantity = minimal_quantity

class OrderHistory:
    """
    Класс для представления истории заказа.

    :param id: ID истории
    :type id: :obj:`int`

    :param state: Состояние заказа
    :type state: :obj:`str`

    :param created_date: Дата создания истории
    :type created_date: :obj:`datetime`
    """
    def __init__(self, id: int, state: str, created_date: datetime):
        self.id = id
        self.state = state
        self.created_date = created_date

    def __str__(self):
        return self.id

class Order:
    """
    Класс для представления заказа.

    :param order_id: ID заказа
    :type order_id: :obj:`str`

    :param customer: Заказчик
    :type customer: :obj:`UserProfile`

    :param quantity: Количество
    :type quantity: :obj:`str`

    :param amount: Сумма
    :type amount: :obj:`str`

    :param seller: Продавец
    :type seller: :obj:`UserProfile`

    :param nickname: Никнейм
    :type nickname: :obj:`str`

    :param state: Состояние заказа
    :type state: :obj:`str`

    :param created_date: Дата создания заказа
    :type created_date: :obj:`datetime`

    :param offer_data: Данные предложения
    :type offer_data: :obj:`OfferData`

    :param reviewed: Был ли заказ проверен
    :type reviewed: :obj:`bool`

    :param offer: Предложение
    :type offer: :obj:`OfferData`

    :param order_history: История заказа
    :type order_history: :obj:`List[OrderHistory]`

    :param transaction: Транзакция
    :type transaction: :obj:`Optional[Dict]`

    :param funds_requested: Запрошены ли средства
    :type funds_requested: :obj:`bool`

    :param deadline: Дедлайн заказа
    :type deadline: :obj:`Optional[datetime]`

    :param auto_delivery: Автоматическая доставка
    :type auto_delivery: :obj:`List`

    :param options: Опции заказа
    :type options: :obj:`List`
    """
    def __init__(self, order_id: str, customer: UserProfile, quantity: str, amount: str, seller: UserProfile,
                 nickname: str, state: str, created_date: datetime, offer_data: OfferData, reviewed: bool,
                 offer: OfferData, order_history: List[OrderHistory], transaction: Optional[Dict], funds_requested: bool,
                 deadline: Optional[datetime], auto_delivery: List, options: List):
        self.order_id = order_id
        self.customer = customer
        self.quantity = quantity
        self.amount = amount
        self.seller = seller
        self.nickname = nickname
        self.state = state
        self.created_date = created_date
        self.offer_data = offer_data
        self.reviewed = reviewed
        self.offer = offer
        self.order_history = order_history
        self.transaction = transaction
        self.funds_requested = funds_requested
        self.deadline = deadline
        self.auto_delivery = auto_delivery
        self.options = options

    def __str__(self):
        return self.order_id


class Notification:
    """
    Класс для представления уведомления.

    :param is_read: Прочитано ли уведомление
    :type is_read: :obj:`bool`

    :param created_date: Дата создания уведомления
    :type created_date: :obj:`datetime`

    :param uuid_id: UUID уведомления
    :type uuid_id: :obj:`str`

    :param verb: Действие уведомления
    :type verb: :obj:`str`

    :param content_id: ID содержимого
    :type content_id: :obj:`str`

    :param title: Заголовок уведомления
    :type title: :obj:`Optional[str]`

    :param date_of_reading: Дата прочтения уведомления
    :type date_of_reading: :obj:`Optional[datetime]`

    :param meta: Мета информация уведомления
    :type meta: :obj:`str`
    """
    def __init__(self, is_read: bool, created_date: datetime, uuid_id: str, verb: str, content_id: str,
                 title: Optional[str], date_of_reading: Optional[datetime], meta: str):
        self.is_read = is_read
        self.created_date = created_date
        self.uuid_id = uuid_id
        self.verb = verb
        self.content_id = content_id
        self.title = title
        self.date_of_reading = date_of_reading
        self.meta = meta

class NotificationList:
    """
    Класс для представления списка уведомлений со страницы - https://paygame.ru/notifications

    :param next: Следующая страница в виде ссылки.
    :type next: :obj:`str`

    :param previous: Предыдущая страница в виде ссылки.
    :type previous: :obj:`str`

    :param next_cursor: Курсор для перехода на след. страницу - (передавать в параметрах запроса ?cursor=)
    :type next_cursor: :obj:`str`

    :param previous_cursor: Курсор для перехода на пред. страницу - (передавать в параметрах запроса ?cursor=)
    :type previous_cursor: :obj:`str`

    :param results: Список уведомлений.
    :type results: :obj: `List[Notification]`
    """
    def __init__(self, next: Optional[str], previous: Optional[str], next_cursor: Optional[str], previous_cursor: Optional[str],
                 results: List[Notification]):
        self.next = next
        self.previous = previous
        self.next_cursor = next_cursor
        self.previous_cursor = previous_cursor
        self.results = results

class NotificationWidget:
    """
    Класс для представления виджета меню последних уведомлений.

    :param next: Следующая страница
    :type next: :obj:`Optional[str]`

    :param previous: Предыдущая страница
    :type previous: :obj:`Optional[str]`

    :param next_cursor: Курсор для следующей страницы
    :type next_cursor: :obj:`Optional[str]`

    :param previous_cursor: Курсор для предыдущей страницы
    :type previous_cursor: :obj:`Optional[str]`

    :param results: Список уведомлений
    :type results: :obj:`List[Notification]`
    """
    def __init__(self, next: Optional[str], previous: Optional[str], next_cursor: Optional[str],
                 previous_cursor: Optional[str], results: List[Notification]):
        self.next = next
        self.previous = previous
        self.next_cursor = next_cursor
        self.previous_cursor = previous_cursor
        self.results = results

class ReviewReply:
    """
    Класс для представления ответа на отзыв.

    :param text: Текст ответа
    :type text: :obj:`str`

    :param date: Дата ответа
    :type date: :obj:`datetime`
    """
    def __init__(self, text: str, date: datetime):
        self.text = text
        self.date = date

class ReviewOffer:
    """
    Класс для представления информации о предложении в отзыве.

    :param id: ID предложения
    :type id: :obj:`int`

    :param game_id: ID игры
    :type game_id: :obj:`int`

    :param game_title: Название игры
    :type game_title: :obj:`str`

    :param offer_type: Тип предложения
    :type offer_type: :obj:`OfferType`
    """
    def __init__(self, id: int, game_id: int, game_title: str, offer_type: OfferType):
        self.id = id
        self.game_id = game_id
        self.game_title = game_title
        self.offer_type = offer_type


class ReviewOrder:
    """
    Класс для представления информации о заказе в отзыве.

    :param id: ID заказа
    :type id: :obj:`int`

    :param state: Состояние заказа
    :type state: :obj:`str`

    :param amount: Сумма заказа
    :type amount: :obj:`str`

    :param offer: Информация о предложении
    :type offer: :obj:`Dict`
    """
    def __init__(self, id: int, state: str, amount: str, offer: Dict):
        self.id = id
        self.state = state
        self.amount = amount
        self.offer = offer

class Review:
    """
    Класс для представления отзыва.

    :param id: ID отзыва
    :type id: :obj:`int`

    :param seller: Продавец (Получатель отзыва)
    :type seller: :obj:`ReviewUser`

    :param author: Автор отзыва
    :type author: :obj:`ReviewUser`

    :param rating: Рейтинг отзыва
    :type rating: :obj:`int`

    :param text: Текст отзыва
    :type text: :obj:`str`

    :param reply: Ответ на отзыв
    :type reply: :obj:`Optional[ReviewReply]`

    :param order: Информация о заказе
    :type order: :obj:`ReviewOrder`

    :param created_date: Дата создания отзыва
    :type created_date: :obj:`datetime`

    :param is_anonymous: Анонимный ли отзыв
    :type is_anonymous: :obj:`bool`

    :param is_included_in_rating: Включен ли отзыв в рейтинг
    :type is_included_in_rating: :obj:`bool`
    """
    def __init__(self, id: int, seller: UserProfile, author: UserProfile, rating: int, text: str,
                 reply: Optional[ReviewReply], order: ReviewOrder, created_date: datetime,
                 is_anonymous: bool, is_included_in_rating: bool):
        self.id = id
        self.seller = seller
        self.author = author
        self.rating = rating
        self.text = text
        self.reply = reply
        self.order = order
        self.created_date = created_date
        self.is_anonymous = is_anonymous
        self.is_included_in_rating = is_included_in_rating


class UserReviews(BasePages):
    """
    Класс описывающий отзывы пользователя.

    :param results: Список отзывов
    :type results: :obj:`List[Review]`
    """
    def __init__(self, results: List[Review], **kwargs):
        super().__init__(results=results, **kwargs)


class OffersGame:
    """
    Класс описывающий предложения по определенной игре

    :param results: Список предложений
    :type results: :obj:`List[OfferData]`
    """
    ...



