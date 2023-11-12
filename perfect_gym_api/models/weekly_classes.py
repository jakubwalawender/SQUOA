from __future__ import annotations
import datetime
from datetime import date
from typing import List, Dict, overload, Iterator, Any

from django.utils.timezone import make_aware
from multimethod import multimethod
from pydantic import BaseModel, Field, RootModel, ValidationError, field_validator, validator

from perfect_gym_api.models.response_base import ResponseBase


class WeeklyClassesRequest(BaseModel):
    club_id: int = Field(alias='clubId')
    start_date: date = Field(alias='date')
    time_table_id: str = Field(alias='timeTableId')
    days_in_week: int = Field(alias='daysInWeek')

    class Config:
        populate_by_name = True

    @field_validator('start_date')
    @classmethod
    def validate_date(cls, value):
        if isinstance(value, date):
            return value
        try:
            res = datetime.datetime.strptime(value, '%Y-%m-%d')
        except Exception as e:
            raise ValidationError("Invalid date format.")
        return res


class ClassRatingSummaryInfo(BaseModel):
    time_table_id: int = Field(alias='TimeTableId')


class ClassPerDayItems(RootModel):
    root: List[ClassPerDay | None]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def remove_empty(self):
        return [x for x in self if self]

    def fits_search(self, start_time: datetime.datetime, time_table_id: int | List[int]) -> False:
        if not self:
            return False
        try:
            date_fits = self[0].start_time == start_time
            if type(time_table_id) == int:
                ttid_fits = self[0].class_rating_summary_info.time_table_id == time_table_id
            else:
                ttid_fits = self[0].class_rating_summary_info.time_table_id in time_table_id
            if ttid_fits and date_fits:
                return True
        except Exception as e:
            return False
        return False


class ClassPerDay(BaseModel):
    id: int = Field(alias='Id')
    start_time: datetime.datetime = Field(alias='StartTime')
    class_rating_summary_info: ClassRatingSummaryInfo = Field(alias='ClassRatingSummaryInfo')

    @field_validator('start_time')
    @classmethod
    def validate_start_time(cls, value):
        if isinstance(value, date):
            return make_aware(value)
        try:
            res = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        except Exception as e:
            raise ValidationError("Invalid date format.")
        return make_aware(res)


class ClassesPerDay(RootModel):
    root: List[ClassPerDayItems]

    def __iter__(self) -> Iterator[ClassPerDayItems]:
        return iter(self.root)

    def __getitem__(self, item) -> ClassPerDayItems:
        return self.root[item]

    def remove_empty(self):
        return [x[0] for x in self.root if x.root]

    def flatten(self):
        return


class ClassesPerHourItem(BaseModel):
    classes_per_day: ClassesPerDay = Field(alias='ClassesPerDay')


class ClassPerDayList(RootModel):
    root: List[ClassPerDay]

    def get(self, start_date: datetime.datetime, time_table_id: int) -> ClassPerDay:
        return next((x for x in self.root if
                     x.start_time == start_date and
                     x.class_rating_summary_info.time_table_id == time_table_id), None)

    def get_multiple(self, start_date: datetime.datetime, time_table_ids: List[int]) -> List[ClassPerDay]:
        results = [x[0] for x in self.root if x.fits_search(time_table_id=time_table_ids, start_time=start_date)]
        return results


class CalendarDataItem(BaseModel):
    classes_per_hour: List[ClassesPerHourItem] = Field(alias='ClassesPerHour')

    def flatten(self) -> ClassPerDayList:
        result = []
        for x in self.classes_per_hour:
            result.extend(x.classes_per_day.remove_empty())
        return ClassPerDayList(root=result)


class WeeklyClassesResponseBody(BaseModel):
    calendar_data: List[CalendarDataItem] = Field(alias='CalendarData')


class WeeklyClassesResponse(ResponseBase):
    body: WeeklyClassesResponseBody

    def get_multiple(self, start_date: datetime.datetime, time_table_ids: List[int]) -> List[ClassPerDay]:
        classes_per_day = self.body.calendar_data[0].classes_per_hour[0].classes_per_day[0].remove_empty()
        results = [x[0] for x in classes_per_day if x.fits_search(time_table_id=time_table_ids, start_time=start_date)]
        return results

    def get(self, start_date: datetime.datetime, time_table_id: int) -> ClassPerDay:
        calendar_data = self.body.calendar_data[0]
        classes = calendar_data.flatten()
        return next((x for x in classes if
                     x.start_time == start_date and
                     x.class_rating_summary_info.time_table_id == time_table_id), None)


class WeeklyClassesTimeTableIdResponses(RootModel):
    root: Dict[str, WeeklyClassesResponse]

    def get_by_id(self, id: str):
        return self.root.get(id, None)

    def flatten(self):
        result = []
        for x in self.root.values():
            calendar_data = x.body.calendar_data[0]
            classes = calendar_data.flatten()
            result.extend(classes.root)
        return ClassPerDayList(root=result)
