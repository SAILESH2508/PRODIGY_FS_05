from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Like, Notification, Hashtag

# Inline admin for Profile
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('bio', 'location', 'birth_date', 'avatar', 'website', 'is_verified')

# Extend User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'is_verified', 'followers_count', 'following_count', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'bio', 'location')
    readonly_fields = ('created_at', 'followers_count', 'following_count')
    
    def followers_count(self, obj):
        return obj.followers_count
    followers_count.short_description = 'Followers'
    
    def following_count(self, obj):
        return obj.following_count
    following_count.short_description = 'Following'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_preview', 'likes_count', 'comments_count', 'is_pinned', 'created_at')
    list_filter = ('is_pinned', 'created_at', 'updated_at')
    search_fields = ('user__username', 'content')
    readonly_fields = ('created_at', 'updated_at', 'likes_count', 'comments_count')
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def likes_count(self, obj):
        return obj.likes_count
    likes_count.short_description = 'Likes'
    
    def comments_count(self, obj):
        return obj.comments_count
    comments_count.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_preview', 'text_preview', 'is_reply', 'created_at')
    list_filter = ('created_at', 'parent')
    search_fields = ('user__username', 'text', 'post__content')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def post_preview(self, obj):
        return f"Post by {obj.post.user.username}"
    post_preview.short_description = 'Post'
    
    def text_preview(self, obj):
        return obj.text[:30] + '...' if len(obj.text) > 30 else obj.text
    text_preview.short_description = 'Comment'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__content')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def post_preview(self, obj):
        return f"Post by {obj.post.user.username}"
    post_preview.short_description = 'Post'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'notification_type', 'message_preview', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'sender__username', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def message_preview(self, obj):
        return obj.message[:40] + '...' if len(obj.message) > 40 else obj.message
    message_preview.short_description = 'Message'

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name', 'posts_count', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'posts_count')
    date_hierarchy = 'created_at'
    
    def posts_count(self, obj):
        return obj.posts_count
    posts_count.short_description = 'Posts Count'

# Customize admin site
admin.site.site_header = "SocialHub Administration"
admin.site.site_title = "SocialHub Admin"
admin.site.index_title = "Welcome to SocialHub Administration"