from django.contrib import admin

from . import models
# Register your models here.

class MessagesInline(admin.TabularInline):
    readonly_fields = ('text', 'create_date', 'channel', 'sender')
    extra = 0
    model = models.Message


class ChannelAdmin(admin.ModelAdmin):

    list_display = ('title', 'started_by', 'create_date',
                    'modify_date', 'is_closed')
    inlines = (MessagesInline,)

admin.site.register(models.Channel, ChannelAdmin)