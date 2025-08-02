from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render
from .models import Message

@cache_page(60)  # cache for 60 seconds
def message_list_view(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
    return render(request, 'chats/message_list.html', {'messages': messages})
