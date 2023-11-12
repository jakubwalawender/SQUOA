import time
from enum import Enum
import copy
from django.utils.translation import gettext_lazy as _

from reservations.models import ActivitySubscription, ActivityType

HOUR_PATTERN = '%H:%M'
HOURS_STRINGS = ['06:30', '07:30', '08:30', '09:30', '10:30',
                 '11:30', '12:30', '13:30', '14:30', '15:30',
                 '16:30', '17:30', '18:30', '19:30', '20:30',
                 '21:30']
WEEKEND_HOURS_INACTIVE = ['06:30', '21:30']


class ReservationHourType(Enum):
    EMPTY = 1
    INACTIVE = 2


DEFAULT_HOURS = [time.strptime(x, HOUR_PATTERN) for x in HOURS_STRINGS]
DAY_HOURS = {0: {hour: ReservationHourType.EMPTY for hour in HOURS_STRINGS},
             1: {hour: ReservationHourType.EMPTY for hour in HOURS_STRINGS},
             2: {hour: ReservationHourType.EMPTY for hour in HOURS_STRINGS},
             3: {hour: ReservationHourType.EMPTY for hour in HOURS_STRINGS},
             4: {hour: ReservationHourType.EMPTY for hour in HOURS_STRINGS},
             5: {
                 hour: (
                     ReservationHourType.EMPTY if hour not in WEEKEND_HOURS_INACTIVE else ReservationHourType.INACTIVE)
                 for hour in HOURS_STRINGS},
             6: {
                 hour: (
                     ReservationHourType.EMPTY if hour not in WEEKEND_HOURS_INACTIVE else ReservationHourType.INACTIVE)
                 for hour in HOURS_STRINGS}
             }


def gather(court):
    result = copy.deepcopy(DAY_HOURS)
    activities = ActivitySubscription.objects.filter(type=court)
    for activity in activities:
        weekday = int(activity.weekday)
        t = activity.hour.time.strftime(HOUR_PATTERN)
        result[weekday][t] = activity
    return result

