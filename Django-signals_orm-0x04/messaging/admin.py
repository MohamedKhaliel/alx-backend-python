from django.contrib import admin
from .models import Message, Notification, MessageHistory

admin.site.register(Message)
admin.site.register(Notification)

class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ('old_content', 'edited_at')

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content', 'edited']
    inlines = [MessageHistoryInline]

admin.site.register(Message, MessageAdmin)
admin.site.register(MessageHistory)
