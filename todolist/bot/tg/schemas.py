from pydantic.main import BaseModel
from typing import List


class Chat(BaseModel):
    id: int


class Message(BaseModel):
    chat: Chat
    text: str or None = None


class UpdateObj(BaseModel):
    update_id: int
    message: Message


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: List[UpdateObj]
