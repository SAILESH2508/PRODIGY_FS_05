# social_app/templatetags/app_filters.py

from django import template

# Register the new tag library
register = template.Library()

@register.filter
def is_liked_by_user(post, user):
    """
    Checks if a post is liked by a specific user.
    Usage: {% with liked_status=post|is_liked_by_user:request.user %}
    """
    # This calls the correct Python model method!
    return post.is_liked_by(user)