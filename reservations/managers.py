from django.db import models



class ActivityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

    def get_queryset_full(self):
        return super().get_queryset()