import time
from typing import Any, Dict, Literal, Optional, Union

from . import enums
from ..types import API_Methods
import cloudscraper
from requests import Response

from .exceptions import UnauthorizedError, RequestFailedError, IncorrectRequest

API_URL_V1 = API_Methods.url_v1

session = cloudscraper.create_scraper()

def _make_request(request_method: Literal["post", "get", "patch"], api_method: str, headers: Dict[str, str] = None,
                  payload: Any = None, requests_delay: int = 0.5, params: Dict[str, Any] = None, files: dict = None,
                  token: Optional[str] = None, timeout: Union[int, float] = 10,
                  raise_not_200: bool = False, refresh_token: bool = False, max_refresh_attempts: int = 1) -> Response:
    """
    Отправляет запрос к API.

    :param request_method: метод запроса ("get" / "post").
    :type request_method: :obj:`str` `post` or `get`

    :param api_method: метод API / полная ссылка.
    :type api_method: :obj:`str`

    :param headers: заголовки запроса.
    :type headers: :obj:`dict`

    :param payload: полезная нагрузка.
    :type payload: :obj:`dict`

    :param params: Параметры запроса.
    :type params: :obj:`dict`

    :param token: токен для авторизации.
    :type token: :obj:`str`, опционально

    :param timeout: таймаут запроса.
    :type timeout: :obj:`int` или :obj:`float`

    :param raise_not_200: возбуждать ли исключение, если статус код ответа != 200?
    :type raise_not_200: :obj:`bool`

    :param refresh_token: Обновлять токен перед выполненеим запроса?
    :type refresh_token: :obj:`bool`

    :param max_refresh_attempts: Максимальное количество попыток обновления токена.
    :type max_refresh_attempts: :obj:`int`

    :return: объект ответа.
    :rtype: :class:`Response`
    """
    attempt = 0
    while attempt <= max_refresh_attempts:
        if refresh_token and token:
            token = _refresh_token(token)
        headers = headers or {}
        if 'User-Agent' not in headers:
            headers[
                'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        if 'Accept' not in headers:
            headers['Accept'] = 'application/json, text/plain, */*'
        if 'Connection' not in headers:
            headers['Connection'] = 'keep-alive'
        if token:
            headers["Cookie"] = f"refreshToken={token}"
            headers["Authorization"] = f"Bearer {token}"

        if not api_method.startswith("https://"):
            api_method = API_URL_V1 + api_method

        time.sleep(requests_delay)
        response = getattr(session, request_method)(
            api_method,
            headers=headers,
            data=payload,
            params=params,
            timeout=timeout,
            files=files
        )

        if response.status_code in (403, 401):
            if attempt < max_refresh_attempts:
                attempt += 1
                refresh_token = True
                continue
            else:
                raise UnauthorizedError(response)
        if response.status_code == 400:
            raise IncorrectRequest(response)
        if response.status_code not in (200, 201):
            raise RequestFailedError(response)

        return response

    raise UnauthorizedError("Исчерпано максимально кол-во попыток обновления токена")


def _refresh_token(token: str) -> str:
    """
    Обновляет токен.

    :param token: текущий токен
    :return: новый токен
    """
    payload = {
        "refresh": token
    }
    response = _make_request("post", API_Methods.refresh, token=token, payload=payload, raise_not_200=True)
    return response.json()['access']


def get_user_info(token: str, username: str = None, user_id: int = None) -> Response:
    """
    Получает информацию о пользователе.

    :param username: Ник пользователя
    :param token: токен для авторизации

    :return: Response object
    """
    token = _refresh_token(token)
    params = {}
    if user_id:
        params["id"] = user_id
    if username:
        params["username"] = username
    return _make_request("get", "profile/user/", params=params, token=token, raise_not_200=True)


def get_me(api_method: str, headers: Dict[str, str], token: str) -> Response:
    """
    Получает информацию о текущем пользователе.

    :param api_method: метод API для получения информации о текущем пользователе
    :param headers: заголовки запроса
    :param token: токен для авторизации

    :return: object Response
    """
    return _make_request("get", api_method, headers, token=token, raise_not_200=True)


def upload_image(token: str, image_data: bytes) -> Response:
    """
    Загружает изображение на сервер PayGame

    :param token: токен для авторизации
    :param image_data: байтовые данные изображения

    :return: object Response
    """
    token = _refresh_token(token)
    files = {
        'file': image_data,
    }
    return _make_request("post", "messager/media/", token=token, files=files)


def send_message(token: str, chat: int, message: str = None, image: str = None) -> Response:
    """
    Отправляет сообщение в указанный чат

    :param token: токен для авторизации
    :param chat: ID чата
    :param message: текст сообщения
    :param image: путь к изображению на сервере PayGame для отправки

    :return: object Response
    """
    data = {}
    if message:
        data["text"] = message
    if image:
        data["media"] = image
    token = _refresh_token(token)
    return _make_request("post", f"messager/{chat}/add/", payload=data,
                         raise_not_200=True, token=token)


def get_order(token: str, order_id: str):
    """
    Получает информацию о заказе

    :param token: токен для авторизации
    :param order_id: ID заказа

    :return: object Response
    """
    token = _refresh_token(token)
    return _make_request("get", f"orders/order/{order_id}/detail/", token=token)


def get_all_notifications(token: str, page_size: int = 10, verb: enums.NotificationTypes = None,
                          cursor: str = None) -> Response:
    """
    Получает все уведомления

    :param page_size: кол-во уведомлений на 1 странице
    :param verb: тип уведомления
    :param cursor: курсор для пагинации
    :param token: токен для авторизации

    :return: object Response
    """
    params = {
        "page_size": page_size
    }
    if verb:
        params["verb"] = verb
    if cursor:
        params["cursor"] = cursor
    return _make_request("get", "notifications/", params=params, token=token)


def get_latest_notifications(token: str) -> Response:
    """
    Получает последние уведомления

    :param token: токен для авторизации

    :return: object Response
    """
    return _make_request("get", "notifications/latest-notifications/", token=token)


def read_messages(token: str, chat_id: int) -> Response:
    """
    Читает сообщения в чате

    :param token: токен для авторизации
    :param chat_id: ID чата

    :return: object Response
    """
    return _make_request("post", f"messager/{chat_id}/read/", token=token)


def get_chat_messages(token: str, chat_id: int, page_size: int = 25) -> Response:
    """
    Получает сообщения из чата

    :param token: токен для авторизации
    :param chat_id: ID чата
    :param page_size: количество сообщений на странице

    :return: object Response
    """
    params = {"id": chat_id, "page_size": page_size}
    return _make_request("get", f"messager/detail/", token=token, params=params)


def mark_all_as_read(token: str) -> Response:
    """
    Помечает все уведомления как прочитанные

    :param token: токен для авторизации

    :return: object Response
    """
    return _make_request("post", "notifications/mark-all-as-read/", token=token)


def get_messager(token: str):
    """
    Получает информацию о мессенджере, в том числе список чатов

    :param token: токен для авторизации

    :return: object Response
    """
    return _make_request("get", "messager/", token=token)


def get_reviews(token: str, username: str, page: int = 1) -> Response:
    """
    :param token: токен для аавторизации
    :param username: юзернейм пользователя
    
    :return: объект Response
    """
    token = _refresh_token(token)
    data = {"username": username}
    return _make_request("get", f"orders/review/{username}/", params={"page": page}, token=token, payload=data)


def reply_to_review(token: str, review_id: int, text: str, edit: bool = False) -> Response:
    """
    Отвечает на отзыв

    :param token: токен для авторизации
    :param review_id: ID отзыва
    :param text: текст ответа
    :param edit: если True, ответ редактируется, иначе - создается новый ответ

    :return: object Response
    """
    data = {"reply": text}
    method = f"orders/review/reply/{review_id}/"
    if edit:
        method += "edit/"
    return _make_request("patch", method, token=token, payload=data)


def change_data(token: str, em_not: bool = False, tg_ap: bool = True, tg_not: bool = True, brwsr_not: bool = False,
                tg_wio: bool = False):
    """
    Изменение настроек уведомлений профиля

    :param em_not: уведомления на почту
    :param tg_ap: уведомления в телеграм
    :param tg_not: уведомление в телеграм, если юзер пингует
    :param brwsr_not: уведомления в барузере (тестовая функция)
    :param tg_wio: уведомление "даже когда я онлайн"

    :return: object Response
    """
    payload = {
        "email_notifications": em_not,
        "telegram_allow_ping": tg_ap,
        "telegram_notification": tg_not,
        "browser_notifications": brwsr_not,
        "telegram_when_i_online": tg_wio
    }
    return _make_request("patch", API_Methods.change_data, payload=payload,
                             token=token)


def change_password(token: str, old_password: str, new_password: str) -> Response:
    """
    Меняет пароль на аккаунте

    :param token: str - токен
    :param old_password: str - старый пароль
    :param new_password: str - новый пароль

    :return: object Response
    """
    data = {
        "old_password": old_password,
        "password": new_password,
        "re_password": new_password
    }
    return _make_request("post", "user/password/change-password/", token=token, payload=data)



