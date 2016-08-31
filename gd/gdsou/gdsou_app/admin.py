from django.contrib import admin
from gdsou_app.models import Zixun,Vipuser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Zixun)

class VipuserInline(admin.StackedInline):
    model = Vipuser
    can_delete = False
    verbose_name_plural = 'vipuser'

class UserAdmin(UserAdmin):
    inlines = (VipuserInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
