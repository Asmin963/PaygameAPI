import requests


class RequestFailedError(Exception):
    """
    Исключение, которое возбуждается, если статус код ответа != 200.
    """
    def __init__(self, response: requests.Response):
        """
        :param response: объект ответа.
        """
        self.response = response
        self.status_code = response.status_code
        self.url = response.request.url
        self.request_headers = response.request.headers
        if "cookie" in self.request_headers:
            self.request_headers["cookie"] = "HIDDEN"
        self.request_body = response.request.body
        self.log_response = False

    def short_str(self):
        return f"Ошибка запроса к {self.url}. (Статус-код: {self.status_code})"

    def __str__(self):
        msg = f"Ошибка запроса к {self.url} .\n" \
              f"Метод: {self.response.request.method} .\n" \
              f"Статус-код ответа: {self.status_code} .\n" \
              f"Заголовки запроса: {self.request_headers} .\n" \
              f"Тело запроса: {self.request_body} .\n" \
              f"Текст ответа: {self.response.text}"
        if self.log_response:
            msg += f"\n{self.response.content.decode()}"
        return msg


class UnauthorizedError(RequestFailedError):
    """
    Исключение, которое возбуждается, если не удалось найти идентифицирующий аккаунт элемент и / или произошло другое
    событие, указывающее на отсутствие авторизации.
    """
    def __init__(self, response):
        super(UnauthorizedError, self).__init__(response)

    def short_str(self):
        return "Не авторизирован (возможно, введен неверный refreshToken)."




class JSONDecodeError(RequestFailedError):
    """
    Исключение, которое возбуждается, если ответ не может быть преобразован в JSON.
    """
    def __init__(self, response):
        super(JSONDecodeError, self).__init__(response)

    def short_str(self):
        return "Ошибка преобразования ответа в JSON."

    def __str__(self):
        return f"Ошибка преобразования ответа в JSON для запроса к {self.url}. (Статус-код: {self.status_code})"

class PayGameAPIError(Exception):
    """
    Базовое исключение для PayGameAPI.
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def short_str(self):
        return "Неверный запрос"

    def __str__(self):
        return self.message


class IncorrectRequest(PayGameAPIError):
    """
    Исключение, которое возбуждается, если запрос не соответствует ожидаемому формату.
    """
    def __init__(self, response):
        super().__init__(response)
        json = response.json()
        self.message = f"Неверный запрос: {json}"

    def __str__(self):
        return self.message

