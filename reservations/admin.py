import pickle
import codecs

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django_celery_results.admin import ALLOW_EDITS
from django_celery_results.models import TaskResult, GroupResult
from pydantic import ValidationError
from unfold.admin import ModelAdmin
from reservations.models import ActivitySubscription, ActivityType, Hour, ActivitySubscriptionProxy
from django_celery_beat.models import PeriodicTask, SolarSchedule, IntervalSchedule, ClockedSchedule, CrontabSchedule
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(ActivitySubscription)
class ActivitySubscriptionAdmin(ModelAdmin):
    list_display = ['id', 'weekday', 'hour', 'type', 'active']
    list_filter = ['weekday', 'type', 'active']

    def get_queryset(self, request):
        qs = ActivitySubscriptionProxy.objects.get_queryset_full()
        return qs


class ActivitySubscriptionProxyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(id=user.id)
        self.fields['hour'].queryset = Hour.objects.all().order_by('time')
        self.fields['user'].initial = self.fields['user'].queryset[0]
        self.fields['user'].disabled = True

    def clean(self):
        # data from the form is fetched using super function
        super(ActivitySubscriptionProxyForm, self).clean()
        if self.cleaned_data.get('user') != self.request.user:
            self._errors['user'] = self.error_class([_("You can only make reservations for yourself!")])
        return self.cleaned_data

    class Meta:
        model = ActivitySubscriptionProxy
        fields = '__all__'


@admin.register(ActivitySubscriptionProxy)
class ActivitySubscriptionProxyAdmin(ModelAdmin):
    list_display = ['id', 'weekday', 'hour', 'type', 'active']
    list_filter = ['weekday', 'type', 'active']
    # search_fields = ['weekday', 'hour__time', 'type__name']
    form = ActivitySubscriptionProxyForm

    def get_queryset(self, request):
        qs = ActivitySubscriptionProxy.objects.get_queryset_full()
        return qs.filter(user=request.user)

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.request = request
        return form


@admin.register(ActivityType)
class ActivityTypeAdminClass(ModelAdmin):
    pass


@admin.register(Hour)
class HourAdmin(ModelAdmin):
    pass


admin.site.unregister(PeriodicTask)
admin.site.unregister(SolarSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(ModelAdmin):
    pass


class TaskResultAdmin(ModelAdmin):
    """Admin-interface for results of tasks."""

    model = TaskResult
    date_hierarchy = 'date_done'
    list_display = ('task_id', 'periodic_task_name', 'task_name', 'date_done',
                    'status', 'worker')
    list_filter = ('status', 'date_done', 'periodic_task_name', 'task_name',
                   'worker')
    readonly_fields = ('date_created', 'date_done', 'result', 'meta')
    search_fields = ('task_name', 'task_id', 'status', 'task_args',
                     'task_kwargs')
    fieldsets = (
        (None, {
            'fields': (
                'task_id',
                'task_name',
                'periodic_task_name',
                'status',
                'worker',
                'content_type',
                'content_encoding',
            ),
            'classes': ('extrapretty', 'wide')
        }),
        (_('Parameters'), {
            'fields': (
                'task_args',
                'task_kwargs',
            ),
            'classes': ('extrapretty', 'wide')
        }),
        (_('Result'), {
            'fields': (
                'result',
                'date_created',
                'date_done',
                'traceback',
                'meta',
            ),
            'classes': ('extrapretty', 'wide')
        }),
    )

    #
    # def get_result(self, item):
    #     return pickle.loads(codecs.decode(item.result.encode(), "base64")).get()

    def get_readonly_fields(self, request, obj=None):
        if ALLOW_EDITS:
            return self.readonly_fields
        else:
            return list({
                field.name for field in self.opts.local_fields
            })


@admin.register(TaskResult)
class TaskResultAdmin(TaskResultAdmin):
    pass


@admin.register(GroupResult)
class GroupResultAdmin(ModelAdmin):
    pass
