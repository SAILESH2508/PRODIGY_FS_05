from django.db import models
from django.contrib.auth.models import User # Correct, single import
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- 1. User Profiles ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # Many-to-Many for following (A follows B, B doesn’t auto-follow A)
    follows = models.ManyToManyField(
        'self',
        related_name='followers',
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.user.username


# --- Signals to manage Profile object lifecycle ---

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # 1. Create Profile only when a new User is created
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # 2. Save the Profile whenever the User object is saved (for updates)
    # The try/except is often added here for robustness in real applications
    if hasattr(instance, 'profile'):
        instance.profile.save()


# --- 2. Posts ---
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_liked_by(self, user):
        """Checks if a given user has liked this post."""
        # Note: self.likes is the related manager for the 'Like' model
        return self.likes.filter(user=user).exists()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.user.username}"


# --- 3. Comments ---
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"


# --- 4. Likes ---
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Crucial constraint: A user can like a post only once
        unique_together = ('user', 'post') 

    def __str__(self):
        return f"{self.user.username} likes Post {self.post.id}"