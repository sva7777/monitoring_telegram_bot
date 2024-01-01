from pydantic import BaseModel
from enum import Enum


class MonitoringTools(str, Enum):
    ping = "ping"


class TelegramChatData(BaseModel):
    token: str
    chat_id: int
    ip_address: str
    tool: MonitoringTools
