from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Message

@login_required
def message_list(request):
    user = request.user
    # users you have chatted with (either direction)
    sent_to_ids = Message.objects.filter(sender=user).values_list('receiver_id', flat=True)
    received_from_ids = Message.objects.filter(receiver=user).values_list('sender_id', flat=True)
    contact_ids = set(list(sent_to_ids) + list(received_from_ids))

    if contact_ids:
        contacts = User.objects.filter(id__in=contact_ids).exclude(id=user.id).order_by('username')
    else:
        # no chats yet -> show everyone (except yourself)
        contacts = User.objects.exclude(id=user.id).order_by('username')

    return render(request, 'message_list.html', {'contacts': contacts})

@login_required
def message_thread(request, user_id):
    other = get_object_or_404(User, id=user_id)
    user = request.user

    # load conversation both directions
    msgs = Message.objects.filter(
        Q(sender=user, receiver=other) | Q(sender=other, receiver=user)
    ).order_by('timestamp')

    # mark messages from 'other' as read
    Message.objects.filter(sender=other, receiver=user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        content = (request.POST.get('content') or '').strip()
        if content:
            Message.objects.create(sender=user, receiver=other, content=content)
        return redirect('message:thread', user_id=other.id)

    return render(request, 'thread.html', {'other': other, 'messages': msgs})
