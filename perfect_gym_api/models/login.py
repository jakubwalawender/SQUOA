from typing import List

from pydantic import Field, ConfigDict, RootModel
from pydantic import BaseModel

from perfect_gym_api.models.response_base import ResponseBase


class LoginRequest(BaseModel):
    login: str = Field(alias="Login")
    password: str = Field(alias="Password")
    remember_me: bool = Field(default=False, alias="RememberMe")

    model_config = ConfigDict(
        populate_by_name=True,
    )


class LoginResponseMember(BaseModel):
    id: int = Field(alias='Id')
    user_number: str = Field(alias='UserNumber')


class LoginResponseUser(BaseModel):
    member: LoginResponseMember = Field(alias='Member')


class LoginResponseError(BaseModel):
    message: str = Field(alias='Message')


class LoginResponseErrors(RootModel):
    root: List[LoginResponseError] | None


class LoginResponseBody(BaseModel):
    user: LoginResponseUser | None = Field(default=None, alias='User')
    errors: LoginResponseErrors | None = Field(default=None, alias='Errors')

    class Meta:
        allow_population_by_field_name = True


class LoginResponseHeaders(BaseModel):
    set_cookie: str | None = Field(alias='Set-Cookie')


class LoginResponse(ResponseBase):
    body: LoginResponseBody
    headers: LoginResponseHeaders
