from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q # Used for complex lookups
from django.urls import reverse
from .models import Post, Like, Profile, Comment
from django.contrib.auth.models import User 
from django.shortcuts import get_object_or_404, redirect # Already there, just a reminder

@login_required
def feed_view(request):
    """
    Displays a personalized feed: posts from users the current user follows, 
    plus the current user's own posts.
    """
    # 1. Get the list of users that the current user is following
    # request.user.profile.follows.all() gives us a queryset of Profile objects 
    # that the current user follows.
    followed_profiles = request.user.profile.follows.all()
    
    # 2. Extract the User objects from the Profile objects
    followed_users = [profile.user.id for profile in followed_profiles]
    
    # 3. Add the current user's ID to the list
    followed_users.append(request.user.id)
    
    # 4. Filter Posts where the user ID is in our list
    # Use __in lookup: Post.objects.filter(user_id__in=followed_users)
    feed_posts = Post.objects.filter(user_id__in=followed_users).order_by('-created_at')
    
    context = {
        'posts': feed_posts
    }
    return render(request, 'social_app/feed.html', context)


@login_required
def like_post_toggle(request, post_id):
    """
    Handles the liking and unliking of a post (used for AJAX/Forms).
    """
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    # Check if a Like object already exists
    like_query = Like.objects.filter(user=user, post=post)
    
    if like_query.exists():
        # User is UNLIKING: Delete the existing Like
        like_query.delete()
    else:
        # User is LIKING: Create a new Like
        Like.objects.create(user=user, post=post)
        
    # Redirect back to the page the user came from
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


@login_required
def profile_view(request, username):
    """
    Displays a user's profile and allows following/unfollowing.
    """
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)
    
    # Check if the logged-in user is following this profile
    is_following = request.user.profile.follows.filter(user=profile_user).exists()
    
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': profile_user.posts.all(), # Access posts via the related_name
        'is_following': is_following,
    }
    return render(request, 'social_app/profile.html', context)


@login_required
def follow_user_toggle(request, username):
    """
    Handles the following and unfollowing of a user.
    """
    target_user = get_object_or_404(User, username=username)
    
    # Check if the user is trying to follow themselves
    if request.user == target_user:
        # Prevent self-following (optional, but good practice)
        return redirect('profile', username=username) 

    target_profile = target_user.profile
    current_user_profile = request.user.profile

    if current_user_profile.follows.filter(user=target_user).exists():
        # User is UNFOLLOWING: Remove the target profile from the 'follows' set
        current_user_profile.follows.remove(target_profile)
    else:
        # User is FOLLOWING: Add the target profile to the 'follows' set
        current_user_profile.follows.add(target_profile)

    return redirect('profile', username=username)

# social_app/views.py (Add this import)
from django.views.generic.edit import CreateView 

# social_app/views.py (Add this class)
class PostCreateView(CreateView):
    model = Post
    # We only allow users to submit the 'content' field
    fields = ['content'] 
    template_name = 'social_app/post_create.html'
    
    # This function automatically sets the 'user' field 
    # of the Post object to the currently logged-in user.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # Define where to redirect the user after a successful post submission
    def get_success_url(self):
        # Redirect to the main feed after posting
        return reverse('feed')

# NOTE: You need to import 'reverse' at the top of views.py: 

# social_app/views.py (Add this function)
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from social_app.forms import CommentForm 

@login_required
def add_comment_to_post(request, post_id):
    """
    Handles the creation of a new comment linked to a specific post.
    """
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # 1. Don't save to database yet (commit=False)
            comment = form.save(commit=False)
            
            # 2. Attach the required Foreign Keys (user and post)
            comment.user = request.user
            comment.post = post
            
            # 3. Save the comment to the database
            comment.save()
            
            # 4. Redirect back to the post detail or feed
            return redirect('feed') # Or redirect to the post's detail view
    
    # If not a POST request, or form is invalid, simply redirect or handle error
    return redirect('feed')

# social_app/views.py (Ensure this function is present)

from django.contrib.auth import login
from django.shortcuts import render, redirect
from social_app.forms import UserRegisterForm # Ensure this is imported

# ... (other view imports and functions) ...

def register_view(request):
    if request.method == 'POST':
        # Make sure you are using the correct form name here!
        form = UserRegisterForm(request.POST) 
        if form.is_valid():
            user = form.save()
            # Log the new user in immediately after registration
            login(request, user) 
            return redirect('feed')
    else:
        form = UserRegisterForm()
    
    context = {'form': form}
    return render(request, 'social_app/register.html', context)