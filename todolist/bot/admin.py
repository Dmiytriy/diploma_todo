from django.contrib import admin

from todolist.bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user')
    readonly_fields = ('verification_code', )
