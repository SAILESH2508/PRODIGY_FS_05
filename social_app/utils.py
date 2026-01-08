import re
from django.contrib.auth.models import User
from .models import Hashtag, Notification

def extract_hashtags(text):
    """Extract hashtags from text and return a list of hashtag names."""
    hashtag_pattern = r'#(\w+)'
    return re.findall(hashtag_pattern, text.lower())

def extract_mentions(text):
    """Extract @mentions from text and return a list of usernames."""
    mention_pattern = r'@(\w+)'
    return re.findall(mention_pattern, text.lower())

def process_post_content(post):
    """Process post content to extract and save hashtags and mentions."""
    # Extract hashtags
    hashtag_names = extract_hashtags(post.content)
    for hashtag_name in hashtag_names:
        hashtag, created = Hashtag.objects.get_or_create(name=hashtag_name)
        hashtag.posts.add(post)

    # Extract mentions and create notifications
    mentioned_usernames = extract_mentions(post.content)
    for username in mentioned_usernames:
        try:
            mentioned_user = User.objects.get(username=username)
            if mentioned_user != post.user:  # Don't notify self
                Notification.objects.create(
                    recipient=mentioned_user,
                    sender=post.user,
                    notification_type='mention',
                    post=post,
                    message=f"{post.user.username} mentioned you in a post"
                )
        except User.DoesNotExist:
            continue

def create_notification(recipient, sender, notification_type, message, post=None, comment=None):
    """Create a notification for a user."""
    if recipient != sender:  # Don't notify self
        Notification.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            post=post,
            comment=comment,
            message=message
        )

def format_post_content(content):
    """Format post content to make hashtags and mentions clickable."""
    # Make hashtags clickable
    content = re.sub(
        r'#(\w+)',
        r'<a href="/hashtag/\1/" class="hashtag-link">#\1</a>',
        content
    )
    
    # Make mentions clickable
    content = re.sub(
        r'@(\w+)',
        r'<a href="/profile/\1/" class="mention-link">@\1</a>',
        content
    )
    
    return content