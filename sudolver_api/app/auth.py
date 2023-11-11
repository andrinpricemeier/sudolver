import secrets


class Authenticator:
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def authenticate(self, user_token: str) -> bool:
        return secrets.compare_digest(user_token, self.api_token)
