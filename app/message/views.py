from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from feedapp.models import Post
from django.contrib import messages as django_messages
from django.http import JsonResponse

@login_required
def message_list(request):
    user = request.user
    # conversations are one-per pair per listing. gather unique (other_user, post)
    sent_pairs = Message.objects.filter(sender=user).values_list('receiver_id', 'post_id').distinct()
    received_pairs = Message.objects.filter(receiver=user).values_list('sender_id', 'post_id').distinct()

    pairs = set(list(sent_pairs) + list(received_pairs))

    # build objects for template: {user: <User>, post: <Post or None>}
    if not pairs:
        contacts = []
    else:
        user_ids = {p[0] for p in pairs}
        post_ids = {p[1] for p in pairs if p[1]}

        users = {u.id: u for u in User.objects.filter(id__in=user_ids)}
        posts = {p.id: p for p in Post.objects.filter(id__in=post_ids)}

        contacts = []
        for other_id, post_id in sorted(pairs, key=lambda t: (t[0], t[1] or 0)):
            contacts.append({'user': users.get(other_id), 'post': posts.get(post_id)})
    # no chats yet -> contacts already empty

    return render(request, 'message_list.html', {'contacts': contacts})

@login_required
def message_thread(request, user_id, post_id=None):
    other = get_object_or_404(User, id=user_id)
    user = request.user
    post = None
    if post_id:
        post = get_object_or_404(Post, id=post_id)

    # load conversation both directions
    # Only show messages matching the listing (post) when post is provided.
    base_q = Q(sender=user, receiver=other) | Q(sender=other, receiver=user)
    if post:
        msgs = Message.objects.filter(base_q, post=post).order_by('timestamp')
    else:
        msgs = Message.objects.filter(base_q).order_by('timestamp')

    # mark messages from 'other' as read
    if post:
        Message.objects.filter(sender=other, receiver=user, is_read=False, post=post).update(is_read=True)
    else:
        Message.objects.filter(sender=other, receiver=user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        content = (request.POST.get('content') or '').strip()
        image_file = request.FILES.get('image')
        image_url = (request.POST.get('image_url') or '').strip()

        # create a message if there is content, an uploaded image, or an image_url
        if content or image_file or image_url:
            m = Message(sender=user, receiver=other, content=content, post=post)
            if image_file:
                m.image = image_file
            elif image_url:
                m.image_url = image_url
            m.save()
        if post:
            return redirect('message:thread_with_post', user_id=other.id, post_id=post.id)
        return redirect('message:thread', user_id=other.id)

    return render(request, 'thread.html', {'other': other, 'messages': msgs, 'post': post})


@login_required
def post_status(request, user_id, post_id):
    """Allow the seller to mark a post sold to the chatter or mark it unavailable.

    This is separate from sending a message; it only updates the Post model
    using the Post.mark_sold and Post.mark_unavailable helpers.
    """
    other = get_object_or_404(User, id=user_id)
    post = get_object_or_404(Post, id=post_id)

    # only the author can change the post status
    if request.user != post.author:
        django_messages.error(request, "Only the seller may change this listing's status.")
        return redirect('message:thread_with_post', user_id=other.id, post_id=post.id)

    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip()
        if action == 'mark_sold':
            # mark as sold to the other user
            post.mark_sold(other)
            django_messages.success(request, f"{post.title} marked as sold to {other.nickname or other.username}.")
        elif action == 'mark_unavailable':
            post.mark_unavailable()
            django_messages.success(request, f"{post.title} marked as unavailable.")

    return redirect('message:thread_with_post', user_id=other.id, post_id=post.id)

@login_required
def message_preview(request):
    return render(request, 'message_preview.html')


@login_required
def unread_messages(request):

    user = request.user
    # newest first
    msgs = Message.objects.filter(receiver=user, is_read=False).select_related('sender', 'post').order_by('-timestamp')

    return render(request, 'message_unread_list.html', {'messages': msgs})

# Return JSON with unread message count for current user
@login_required
def unread_count_api(request):
    count = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()
    return JsonResponse({"unread_count": count})
