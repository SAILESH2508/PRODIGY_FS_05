from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Exists, OuterRef, Count
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.db import IntegrityError
from django.conf import settings
import logging

from .models import Post, Like, Profile, Comment, Notification, Hashtag
from django.contrib.auth.models import User
from .forms import (
    UserRegisterForm, CommentForm, ProfileUpdateForm, 
    PostCreateForm, UserUpdateForm, ReplyForm
)
from .utils import process_post_content, create_notification

logger = logging.getLogger(__name__)


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'social_app/profile_update.html', context)


@login_required
def feed_view(request):
    """Displays a global feed with all posts from all users."""
    
    # Show ALL posts from ALL users (global feed)
    posts = Post.objects.all().annotate(
        is_liked_by_user=Exists(Like.objects.filter(user=request.user, post=OuterRef('pk')))
    ).select_related('user', 'user__profile').prefetch_related(
        'comments__user', 'likes', 'hashtags'
    ).order_by('-is_pinned', '-created_at')
    
    # Pagination
    paginator = Paginator(posts, getattr(settings, 'POSTS_PER_PAGE', 10))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'feed_type': 'global'
    }
    return render(request, 'social_app/feed.html', context)


@login_required
def following_feed_view(request):
    """Displays a personalized feed with posts from followed users only."""
    followed_profiles = request.user.profile.follows.all()
    followed_users = [profile.user.id for profile in followed_profiles]
    followed_users.append(request.user.id)  # Include own posts
    
    posts = Post.objects.filter(user_id__in=followed_users).annotate(
        is_liked_by_user=Exists(Like.objects.filter(user=request.user, post=OuterRef('pk')))
    ).select_related('user', 'user__profile').prefetch_related(
        'comments__user', 'likes', 'hashtags'
    ).order_by('-is_pinned', '-created_at')
    
    # Pagination
    paginator = Paginator(posts, getattr(settings, 'POSTS_PER_PAGE', 10))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'feed_type': 'following'
    }
    return render(request, 'social_app/feed.html', context)


@login_required
# @require_POST - Temporarily disabled to allow GET request from anchor tag
@csrf_protect
def like_post_toggle(request, post_id):
    """AJAX endpoint for liking/unliking posts."""
    try:
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        
        like_query = Like.objects.filter(user=user, post=post)
        
        if like_query.exists():
            like_query.delete()
            liked = False
            # Remove like notification if exists
            Notification.objects.filter(
                recipient=post.user,
                sender=user,
                notification_type='like',
                post=post
            ).delete()
        else:
            Like.objects.create(user=user, post=post)
            liked = True
            # Create like notification
            create_notification(
                recipient=post.user,
                sender=user,
                notification_type='like',
                message=f"{user.username} liked your post",
                post=post
            )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'liked': liked,
                'likes_count': post.likes.count()
            })
        
        return redirect(request.META.get('HTTP_REFERER', 'feed'))
    
    except Exception as e:
        logger.error(f"Error in like_post_toggle for user {request.user.username}: {e}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'An error occurred'}, status=500)
        messages.error(request, 'An error occurred while processing your request.')
        return redirect('feed')


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)
    is_following = request.user.profile.follows.filter(user=profile_user).exists()
    
    posts = profile_user.posts.annotate(
        is_liked_by_user=Exists(Like.objects.filter(user=request.user, post=OuterRef('pk')))
    ).select_related('user').prefetch_related(
        'comments__user', 'likes', 'hashtags'
    ).order_by('-is_pinned', '-created_at')
    
    # Pagination for profile posts
    paginator = Paginator(posts, getattr(settings, 'POSTS_PER_PAGE', 10))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'is_following': is_following,
    }
    return render(request, 'social_app/profile.html', context)


@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()
    users = []
    posts = []
    hashtags = []
    
    # Validate query length to prevent abuse
    if len(query) > 100:
        messages.error(request, 'Search query is too long. Please use fewer than 100 characters.')
        query = query[:100]
    
    if query and len(query) >= 2:  # Minimum 2 characters for search
        # Search users
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(profile__bio__icontains=query)
        ).select_related('profile').distinct()[:10]
        
        # Search posts
        posts = Post.objects.filter(content__icontains=query).annotate(
            is_liked_by_user=Exists(Like.objects.filter(user=request.user, post=OuterRef('pk')))
        ).select_related('user', 'user__profile').prefetch_related(
            'comments__user', 'likes', 'hashtags'
        ).order_by('-created_at')[:20]

        # Search hashtags
        if query.startswith('#'):
            hashtag_name = query[1:]  # Remove the # symbol
            hashtags = Hashtag.objects.filter(name__icontains=hashtag_name)[:10]
        else:
            hashtags = Hashtag.objects.filter(name__icontains=query)[:10]
    elif query and len(query) < 2:
        messages.info(request, 'Please enter at least 2 characters to search.')

    # Paginate search results
    paginator = Paginator(posts, getattr(settings, 'POSTS_PER_PAGE', 10))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'users': users,
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'hashtags': hashtags,
    }
    return render(request, 'social_app/search.html', context)


@login_required
def follow_user_toggle(request, username):
    """Handle following/unfollowing users."""
    target_user = get_object_or_404(User, username=username)
    
    if request.user == target_user:
        messages.warning(request, "You cannot follow yourself!")
        return redirect('profile', username=username)

    target_profile = target_user.profile
    current_user_profile = request.user.profile

    if current_user_profile.follows.filter(user=target_user).exists():
        current_user_profile.follows.remove(target_profile)
        messages.success(request, f"You unfollowed {target_user.username}")
        # Remove follow notification
        Notification.objects.filter(
            recipient=target_user,
            sender=request.user,
            notification_type='follow'
        ).delete()
    else:
        current_user_profile.follows.add(target_profile)
        messages.success(request, f"You are now following {target_user.username}")
        # Create follow notification
        create_notification(
            recipient=target_user,
            sender=request.user,
            notification_type='follow',
            message=f"{request.user.username} started following you"
        )

    return redirect('profile', username=username)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'social_app/post_create.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        # Process hashtags and mentions
        process_post_content(self.object)
        
        messages.success(self.request, 'Your post has been shared!')
        return response

    def get_success_url(self):
        return reverse('feed')


@login_required
def add_comment_to_post(request, post_id):
    """Handle adding comments to posts."""
    try:
        post = get_object_or_404(Post, id=post_id)
        
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                
                # Create comment notification
                create_notification(
                    recipient=post.user,
                    sender=request.user,
                    notification_type='comment',
                    message=f"{request.user.username} commented on your post",
                    post=post,
                    comment=comment
                )
                
                messages.success(request, 'Comment added successfully!')
            else:
                for error in form.errors.values():
                    messages.error(request, error[0])
                
            return redirect(request.META.get('HTTP_REFERER', 'feed'))
        
        return redirect('feed')
    
    except Exception as e:
        logger.error(f"Error adding comment for user {request.user.username}: {e}")
        messages.error(request, 'An error occurred while adding your comment.')
        return redirect('feed')


@login_required
def add_reply_to_comment(request, comment_id):
    """Handle adding replies to comments."""
    parent_comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = parent_comment.post
            reply.parent = parent_comment
            reply.save()
            
            # Create reply notification
            create_notification(
                recipient=parent_comment.user,
                sender=request.user,
                notification_type='comment',
                message=f"{request.user.username} replied to your comment",
                post=parent_comment.post,
                comment=reply
            )
            
            messages.success(request, 'Reply added successfully!')
    
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


@login_required
def notifications_view(request):
    """Display user notifications."""
    notifications = request.user.notifications.select_related(
        'sender', 'post', 'comment'
    ).order_by('-created_at')
    
    # Mark notifications as read
    unread_notifications = notifications.filter(is_read=False)
    unread_notifications.update(is_read=True)
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'notifications': page_obj.object_list,
        'page_obj': page_obj
    }
    return render(request, 'social_app/notifications.html', context)


@login_required
def hashtag_view(request, hashtag_name):
    """Display posts for a specific hashtag."""
    hashtag = get_object_or_404(Hashtag, name=hashtag_name.lower())
    
    posts = hashtag.posts.annotate(
        is_liked_by_user=Exists(Like.objects.filter(user=request.user, post=OuterRef('pk')))
    ).select_related('user', 'user__profile').prefetch_related(
        'comments__user', 'likes', 'hashtags'
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(posts, getattr(settings, 'POSTS_PER_PAGE', 10))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'hashtag': hashtag,
        'posts': page_obj.object_list,
        'page_obj': page_obj
    }
    return render(request, 'social_app/hashtag.html', context)


@login_required
def post_detail_view(request, post_id):
    """Display a single post with all comments."""
    post = get_object_or_404(Post, id=post_id)
    
    # Get top-level comments (not replies)
    comments = post.comments.filter(parent=None).select_related(
        'user'
    ).prefetch_related('replies__user').order_by('created_at')
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': CommentForm(),
        'reply_form': ReplyForm(),
    }
    return render(request, 'social_app/post_detail.html', context)


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) 
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f'Account created for {user.username}! You are now logged in.')
                login(request, user) 
                return redirect('feed')
            except IntegrityError:
                form.add_error('username', 'This username is already taken.')
    else:
        form = UserRegisterForm()
    
    context = {'form': form}
    return render(request, 'social_app/register.html', context)


@login_required
def toggle_pin_post(request, post_id):
    """Toggle pin status of a post (only for post owner)."""
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.is_pinned = not post.is_pinned
    post.save()
    
    status = "pinned" if post.is_pinned else "unpinned"
    messages.success(request, f'Post {status} successfully!')
    
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


@login_required
def delete_post(request, post_id):
    """Delete a post (only for post owner)."""
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('profile', username=request.user.username)
    
    return render(request, 'social_app/confirm_delete.html', {'object': post, 'type': 'post'})


@login_required
def unread_notifications_count(request):
    """AJAX endpoint to get unread notifications count."""
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count})