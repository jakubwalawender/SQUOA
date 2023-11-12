from abc import ABC, abstractmethod
from calendar import c
from datetime import date
from typing import List, Tuple
from urllib.parse import urljoin
import requests

from perfect_gym_api.models.book_class import BookClassResponse, BookClassRequest, BookClassResponseBody
from perfect_gym_api.models.login import LoginResponse, LoginRequest, LoginResponseBody, LoginResponseHeaders
from perfect_gym_api.models.settings import PerfectGymSettings
from perfect_gym_api.models.weekly_classes import WeeklyClassesRequest, WeeklyClassesResponse, \
    WeeklyClassesResponseBody, WeeklyClassesTimeTableIdResponses
from perfect_gym_api.helpers import generate_headers


class PerfectGymApiBase(ABC):
    @abstractmethod
    def login(self, username: str, password: str) -> LoginResponse:
        ...

    @abstractmethod
    def weekly_classes(self, start_date: date, days_in_week: int, club_id: int,
                       time_table_id: int) -> WeeklyClassesResponse:
        ...


class PerfectGymApi(PerfectGymApiBase):
    def __init__(self, settings: PerfectGymSettings):
        self.settings = settings
        self.login_url = urljoin(settings.url, settings.login_path)
        self.weekly_classes_url = urljoin(settings.url, settings.weekly_classes_path)
        self.book_class_url = urljoin(settings.url, settings.book_classes_path)

    def login(self, login: str, password: str) -> LoginResponse:
        headers = generate_headers(headers=self.settings.request_headers)
        request = LoginRequest(login=login, password=password)
        payload = request.model_dump_json(by_alias=True)
        response = requests.post(url=self.login_url, headers=headers, data=payload)
        response_body = LoginResponseBody(**response.json())
        response_headers = LoginResponseHeaders(**response.headers)
        result = LoginResponse(body=response_body, headers=response_headers, http_status_code=response.status_code)
        return result

    def weekly_classes(self, start_date: date, days_in_week: int = 10, club_id: int = 4,
                       time_table_id: str = "170") -> WeeklyClassesResponse:
        headers = generate_headers(headers=self.settings.request_headers)
        request = WeeklyClassesRequest(days_in_week=days_in_week, club_id=club_id, time_table_id=time_table_id,
                                       start_date=start_date)
        payload = request.model_dump_json(by_alias=True)
        response = requests.post(url=self.weekly_classes_url, headers=headers, data=payload)
        response_body = WeeklyClassesResponseBody(**response.json())
        result = WeeklyClassesResponse(body=response_body, http_status_code=response.status_code)
        return result

    def multiple_weekly_classes(self, start_date: date, days_in_week: int = 10, club_id: int = 4,
                                time_table_ids: Tuple[str] = ("170", "171")) -> WeeklyClassesTimeTableIdResponses:
        result_dict = {}
        for time_table_id in time_table_ids:
            response = self.weekly_classes(start_date, days_in_week, club_id, time_table_id)
            result_dict[time_table_id] = response
        return WeeklyClassesTimeTableIdResponses(result_dict)

    def book_class(self, class_id: int, login_response: LoginResponse, club_id: str = "4") -> BookClassResponse:
        headers = generate_headers(headers=self.settings.request_headers)
        headers['Cookie'] = f'ClientPortal.Embed;{login_response.headers.set_cookie}'
        request = BookClassRequest(class_id=class_id, club_id=club_id)
        payload = request.model_dump_json(by_alias=True)
        response = requests.post(url=self.book_class_url, headers=headers, data=payload)
        response_body = BookClassResponseBody(**response.json())
        result = BookClassResponse(body=response_body, http_status_code=response.status_code)
        return result
