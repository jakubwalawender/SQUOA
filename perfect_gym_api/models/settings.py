from typing import List

from pydantic import BaseModel, RootModel


class RequestHeaders(BaseModel):
    host: str
    origin: str
    referer: str
    cookie: str

    def set_cookie(self, cookie: str):
        self.cookie = ";".join((self.cookie, cookie))


class PerfectGymSettings(BaseModel):
    request_headers: RequestHeaders
    url: str
    login_path: str
    weekly_classes_path: str
    book_classes_path: str


class Credentials(BaseModel):
    login: str
    password: str


class ReservationsByDays(BaseModel):
    monday: List[str]
    tuesday: List[str]
    wednesday: List[str]
    thursday: List[str]
    friday: List[str]
    saturday: List[str]
    sunday: List[str]


class Reservations(BaseModel):
    timetable_id: str
    days: ReservationsByDays


class ReservationsList(RootModel):
    root: List[Reservations]


class UserPreferences(BaseModel):
    credentials: Credentials
    reservations: ReservationsList | None


class UserPreferencesList(RootModel):
    root: List[UserPreferences] | None


class Settings(BaseModel):
    perfect_gym_settings: PerfectGymSettings
    user_preferences: UserPreferencesList | None
