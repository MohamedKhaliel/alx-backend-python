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


def get_threaded_replies(parent_msg):
    replies = (
        Message.objects
        .filter(parent_message=parent_msg)
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related('replies')
        .order_by('timestamp')
    )
    return [
        {
            'message': reply,
            'replies': get_threaded_replies(reply)
        } for reply in replies
    ]

def show_all_messages(request):
    messages = Message.objects.filter(parent_message=None)
    return render(request, 'messaging/all_messages.html', {'messages': messages})



def unread_messages_view(request):
    user = request.user
    unread_messages = Message.unread.unread_for_user(user).only('id', 'sender', 'content', 'timestamp')
    return render(request, 'messaging/unread_messages.html', {'messages': unread_messages})

