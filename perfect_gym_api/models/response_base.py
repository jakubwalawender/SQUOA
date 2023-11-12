from pydantic import BaseModel


class ResponseBase(BaseModel):
    http_status_code: int
