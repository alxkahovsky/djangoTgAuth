import httpx


class SiteAuthConnector:
    def __init__(self, url: str, auth_username: str = None, auth_password: str = None):
        self.__check_url(url)
        self.url = url
        if auth_username and auth_password:
            self.client = httpx.Client(auth=(auth_username, auth_password))
        else:
            self.client = httpx.Client()

    @staticmethod
    def __check_url(url: str):
        if not url.startswith("http://") or not url.startswith("https://"):
            raise Exception(f"{url} Invalid protocol")
        if not url.endswith("/"):
            raise Exception(f"{url} is not a valid. Try append '/' at the end of the url")

    def __is_telegram_bind(self, telegram_id: str) -> bool:
        """Проверяем связку аккаунта на сайте и телеграм аккаунта"""
        url = f"{self.url}{telegram_id}/"
        response = self.client.get(url)
        if response.status_code != 200:
            return False
        return True

    def __bind_telegram(self, telegram_id: str, telegram_username: str, auth_session_key: str):
        """Привязываем телеграм аккаунт к аккаунту пользователя"""
        data = {"telegram_id": telegram_id, "username": telegram_username, "session": auth_session_key}
        response = self.client.post(self.url, data=data)
        if response.status_code != 201:
            raise Exception(f'Bind telegram error: status: {response.status_code}, message:{response.text}')

    def __update_telegram(self, telegram_id: str, telegram_username: str, auth_session_key: str):
        """Обновляем данные телеграм аккаунта на сайте"""
        data = {"telegram_id": telegram_id, "username": telegram_username, "session": auth_session_key}
        response = self.client.put(f'{self.url}{telegram_id}/', data=data)
        if response.status_code != 200:
            raise Exception(f'Update telegram error: status: {response.status_code}, message:{response.text}')

    def complete_auth(self, telegram_id: str, username: str, session_key: str):
        if self.__is_telegram_bind(telegram_id):
            self.__update_telegram(telegram_id, username, session_key)
        else:
            self.__bind_telegram(telegram_id, username, session_key)
