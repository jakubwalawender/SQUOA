from datetime import datetime, timedelta
from typing import List

from celery import shared_task, group, chain, chord
from django.utils import timezone
from pydantic import BaseModel, ConfigDict, RootModel

from accounts.models import User

from config.settings import RESERVATION_DAYS_FORWARD, PERFECT_GYM_API
from perfect_gym_api.models.login import LoginResponse
from reservations.models import ActivitySubscription


class LoginUserResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    user: User
    result: LoginResponse


class LoginUserResults(RootModel):
    root: List[LoginUserResult]

    def get_result_for_user(self, user):
        return next((x.result for x in self.root if x.user == user), None)


@shared_task
def login_user(id: int) -> LoginUserResult | None:
    try:
        user = User.objects.get(id=id)
        if user.platform_login and user.platform_password:
            login_result = PERFECT_GYM_API.login(login=user.platform_login, password=user.platform_password)
        else:
            return None
        if login_result.body.errors:
            return None
        return LoginUserResult(user=user, result=login_result)
    except User.DoesNotExist as e:
        raise


@shared_task
def login_users_group():
    users = User.objects.all()
    task_group = group([login_user.s(user.id) for user in users])
    return task_group


@shared_task
def make_reservation(id: int, login_response: LoginResponse):
    result = PERFECT_GYM_API.book_class(class_id=id, login_response=login_response)
    return result


@shared_task
def make_reservations_for_date(login_user_results: List[LoginUserResult], reservation_datetime: datetime):
    login_users_results_cleaned = [x for x in login_user_results if x is not None]
    login_users_results_cleaned = LoginUserResults(root=login_users_results_cleaned)
    weekday = str(reservation_datetime.weekday())
    time = reservation_datetime.time()
    activity_subscriptions = ActivitySubscription.objects.filter(weekday=weekday, hour__time=time)
    activities_dict = PERFECT_GYM_API.multiple_weekly_classes(start_date=reservation_datetime.date())
    activities_list = activities_dict.flatten()
    while True:
        if timezone.localtime(timezone.now()).minute == 30:
            break

    task_list = []
    for subscription in activity_subscriptions:
        external_id = int(subscription.type.external_id)
        user = subscription.user
        login_response = login_users_results_cleaned.get_result_for_user(user)
        found = activities_list.get(start_date=reservation_datetime, time_table_id=external_id)
        if not found:
            continue
        task = make_reservation.s(id=found.id, login_response=login_response)
        task_list.append(task)
    task_group = group(task_list)
    result_group = task_group.apply_async()
    return result_group


def get_reservation_datetime(days_forward: int = RESERVATION_DAYS_FORWARD) -> datetime:
    now = timezone.localtime(timezone.now())
    if now.minute < 30:
        result = now.replace(minute=30, second=0, microsecond=0) + timedelta(days=days_forward)
    else:
        result = now.replace(hour=now.hour + 1, minute=0, second=0, microsecond=0) + timedelta(days=days_forward)
    return result


@shared_task
def make_reservations():
    now = timezone.localtime(timezone.now())
    if now.minute < 28 or now.minute > 30:
        return "Forfeiting task - wrong time"
    date = get_reservation_datetime()
    c = chord(login_users_group(), make_reservations_for_date.s(date))
    r = c.apply_async()
    return r
