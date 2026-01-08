from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def format_content(content):
    """Format post content to make hashtags and mentions clickable."""
    # Make hashtags clickable
    content = re.sub(
        r'#(\w+)',
        r'<a href="/hashtag/\1/" class="hashtag-link" style="color: var(--secondary); font-weight: 500;">#\1</a>',
        content
    )
    
    # Make mentions clickable
    content = re.sub(
        r'@(\w+)',
        r'<a href="/profile/\1/" class="mention-link" style="color: var(--accent); font-weight: 500;">@\1</a>',
        content
    )
    
    return mark_safe(content)

@register.filter
def truncate_words_html(value, arg):
    """Truncate text but preserve HTML tags."""
    try:
        length = int(arg)
    except ValueError:
        return value
    
    words = value.split()
    if len(words) <= length:
        return value
    
    truncated = ' '.join(words[:length])
    return mark_safe(f"{truncated}...")

@register.simple_tag
def notification_icon(notification_type):
    """Return appropriate icon for notification type."""
    icons = {
        'like': 'heart',
        'comment': 'chatbubble',
        'follow': 'person-add',
        'mention': 'at',
    }
    return icons.get(notification_type, 'notifications')

@register.simple_tag
def notification_color(notification_type):
    """Return appropriate color for notification type."""
    colors = {
        'like': 'var(--accent)',
        'comment': 'var(--secondary)',
        'follow': 'var(--primary)',
        'mention': 'var(--secondary)',
    }
    return colors.get(notification_type, 'var(--text-muted)')

@register.filter
def user_initial(username):
    """Get the first letter of username in uppercase."""
    return username[0].upper() if username else '?'