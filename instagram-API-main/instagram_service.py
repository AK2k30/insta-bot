from instagrapi import Client
from instagrapi.types import UserShort
from typing import Optional

class InstagramService:
    def __init__(self):
        self.clients = {}

    def login(self, username: str, password: str) -> str:
        client = Client()
        client.login(username, password)
        self.clients[username] = client
        return username

    def get_client(self, username: str) -> Optional[Client]:
        return self.clients.get(username)

    def get_media_likers(self, username: str, media_id: str):
        client = self.get_client(username)
        if client:
            likers = client.media_likers(media_id)
            return [self.user_short_to_dict(liker) for liker in likers]
        else:
            return None

    def user_short_to_dict(self, user_short: UserShort):
        return {
            "pk": user_short.pk,
            "username": user_short.username,
            "full_name": user_short.full_name,
        }

instagram_service = InstagramService()
