from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Message

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('logout')  # or any page you want after deletion


@login_required
def conversation_thread(request, user_id):
    messages = (
        Message.objects
        .filter(sender=request.user, receiver_id=user_id)
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related('replies')
        .order_by('timestamp')
    )
    return render(request, 'messaging/thread.html', {'messages': messages})

def get_replies(message):
    replies = []
    for reply in message.replies.all():
        nested = get_replies(reply)
        replies.append({
            'message': reply,
            'replies': nested
        })
    return replies
