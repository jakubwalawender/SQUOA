from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission, GroupManager
from django.db import models
from unfold.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# admin.site.unregister(Group)
#
#
# @admin.register(Group)
# class GroupAdmin(ModelAdmin):
#     name = models.CharField(_("name"), max_length=150, unique=True)
#     permissions = models.ManyToManyField(
#         Permission,
#         verbose_name=_("permissions"),
#         blank=True,
#     )
#
#     objects = GroupManager()
#
#     class Meta:
#         verbose_name = _("group")
#         verbose_name_plural = _("groups")
#
#     def __str__(self):
#         return self.name
#
#     def natural_key(self):
#         return (self.name,)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ('username', 'platform_login', 'platform_password')
    search_fields = ('username', 'platform_login', 'platform_password')
