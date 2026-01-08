from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from social_app.models import Profile, Post, Comment, Like, Notification, Hashtag
from social_app.forms import PostCreateForm, CommentForm, ProfileUpdateForm
import tempfile
from PIL import Image
import io


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )

    def test_profile_creation(self):
        """Test that profile is created automatically when user is created."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.user, self.user)

    def test_post_creation(self):
        """Test post creation and methods."""
        post = Post.objects.create(
            user=self.user,
            content="Test post content #test @testuser2"
        )
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.content, "Test post content #test @testuser2")
        self.assertFalse(post.is_liked_by(self.user2))

    def test_like_functionality(self):
        """Test like creation and uniqueness."""
        post = Post.objects.create(user=self.user, content="Test post")
        
        # Create like
        like = Like.objects.create(user=self.user2, post=post)
        self.assertTrue(post.is_liked_by(self.user2))
        self.assertEqual(post.likes_count, 1)
        
        # Test unique constraint
        with self.assertRaises(Exception):
            Like.objects.create(user=self.user2, post=post)

    def test_comment_creation(self):
        """Test comment creation and reply functionality."""
        post = Post.objects.create(user=self.user, content="Test post")
        comment = Comment.objects.create(
            user=self.user2,
            post=post,
            text="Test comment"
        )
        
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.user, self.user2)
        self.assertFalse(comment.is_reply)
        
        # Test reply
        reply = Comment.objects.create(
            user=self.user,
            post=post,
            text="Test reply",
            parent=comment
        )
        self.assertTrue(reply.is_reply)
        self.assertEqual(reply.parent, comment)

    def test_follow_functionality(self):
        """Test user following functionality."""
        profile1 = self.user.profile
        profile2 = self.user2.profile
        
        # Follow user
        profile1.follows.add(profile2)
        
        self.assertEqual(profile1.following_count, 1)
        self.assertEqual(profile2.followers_count, 1)
        self.assertIn(profile2, profile1.follows.all())


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )

    def test_feed_view_authenticated(self):
        """Test feed view for authenticated users."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'feed')

    def test_feed_view_unauthenticated(self):
        """Test feed view redirects unauthenticated users."""
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        """Test profile view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_post_creation_view(self):
        """Test post creation."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('post_create'), {
            'content': 'Test post content'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Post.objects.filter(content='Test post content').exists())

    def test_like_toggle_ajax(self):
        """Test AJAX like toggle."""
        self.client.login(username='testuser', password='testpass123')
        post = Post.objects.create(user=self.user2, content="Test post")
        
        response = self.client.post(
            reverse('like_post_toggle', kwargs={'post_id': post.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Like.objects.filter(user=self.user, post=post).exists())

    def test_search_view(self):
        """Test search functionality."""
        self.client.login(username='testuser', password='testpass123')
        Post.objects.create(user=self.user, content="Searchable content")
        
        response = self.client.get(reverse('search'), {'q': 'Searchable'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Searchable content')


class FormTestCase(TestCase):
    def test_post_create_form_valid(self):
        """Test valid post creation form."""
        form_data = {'content': 'Valid post content'}
        form = PostCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_create_form_invalid(self):
        """Test invalid post creation form."""
        form_data = {'content': ''}  # Empty content
        form = PostCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_comment_form_valid(self):
        """Test valid comment form."""
        form_data = {'text': 'Valid comment'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        """Test invalid comment form."""
        form_data = {'text': 'x'}  # Too short
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())


class UtilsTestCase(TestCase):
    def test_hashtag_extraction(self):
        """Test hashtag extraction from text."""
        from social_app.utils import extract_hashtags
        text = "This is a #test post with #multiple #hashtags"
        hashtags = extract_hashtags(text)
        self.assertEqual(set(hashtags), {'test', 'multiple', 'hashtags'})

    def test_mention_extraction(self):
        """Test mention extraction from text."""
        from social_app.utils import extract_mentions
        text = "Hello @user1 and @user2, how are you?"
        mentions = extract_mentions(text)
        self.assertEqual(set(mentions), {'user1', 'user2'})

    def test_post_content_processing(self):
        """Test post content processing for hashtags and mentions."""
        from social_app.utils import process_post_content
        
        user = User.objects.create_user(username='testuser', password='test123')
        mentioned_user = User.objects.create_user(username='mentioned', password='test123')
        
        post = Post.objects.create(
            user=user,
            content="Test post with #hashtag and @mentioned"
        )
        
        process_post_content(post)
        
        # Check hashtag was created
        self.assertTrue(Hashtag.objects.filter(name='hashtag').exists())
        hashtag = Hashtag.objects.get(name='hashtag')
        self.assertIn(post, hashtag.posts.all())
        
        # Check notification was created
        self.assertTrue(
            Notification.objects.filter(
                recipient=mentioned_user,
                sender=user,
                notification_type='mention'
            ).exists()
        )
