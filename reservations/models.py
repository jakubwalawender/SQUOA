from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from reservations.managers import ActivityManager

User = get_user_model()


class ActivityType(models.Model):
    external_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"


class Hour(models.Model):
    time = models.TimeField(unique=True)

    def __str__(self):
        return f"{self.time.strftime('%H:%M')}"


class ActivitySubscription(models.Model):
    class Weekday(models.TextChoices):
        MONDAY = 0, _("Monday")
        TUESDAY = 1, _("Tuesday")
        WEDNESDAY = 2, _("Wednesday")
        THURSDAY = 3, _("Thursday")
        FRIDAY = 4, _("Friday")
        SATURDAY = 5, _("Saturday")
        SUNDAY = 6, _("Sunday")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=2, choices=Weekday.choices, default=Weekday.MONDAY)
    type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    objects = ActivityManager()

    class Meta:
        unique_together = (("hour", "weekday", "type"), ("user", "weekday", "hour"))
        verbose_name_plural = _("activity subscriptions")

    def __str__(self):
        return f"{self.type.name} - {self.hour} - {self.weekday}"


class ActivitySubscriptionProxy(ActivitySubscription):
    class Meta:
        proxy = True
        verbose_name = "activity subscription proxy"
        verbose_name_plural = _("activity subscription proxys")
