from pydantic import BaseModel


class TelegramChatData(BaseModel):
    token: str
    chat_id: int



