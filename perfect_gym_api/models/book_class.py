from typing import List
from pydantic import BaseModel, Field, ConfigDict

from perfect_gym_api.models.response_base import ResponseBase


class BookClassRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    class_id: int = Field(alias='classId')
    club_id: str = Field(alias='clubId')


class BookClassResponseError(BaseModel):
    message: str = Field(alias='Message')


class BookClassResponseBody(BaseModel):
    errors: List[BookClassResponseError] | None = Field(None,alias='Errors')
    class_id: int | None = Field(None,alias='ClassId')
    user_id: int | None = Field(None,alias='UserId')


class BookClassResponse(ResponseBase):
    body: BookClassResponseBody
