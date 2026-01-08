from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from social_app.models import Comment, Profile, Post

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Add a comment...',
                'class': 'form-control',
                'autocomplete': 'off',
                'maxlength': '500'
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text or not text.strip():
            raise forms.ValidationError("Comment cannot be empty.")
        if len(text.strip()) < 2:
            raise forms.ValidationError("Comment must be at least 2 characters long.")
        return text.strip()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'first_name', 'last_name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Clear help text for username
        if 'username' in self.fields:
            self.fields['username'].help_text = ''
        
        # Clear help text for passwords
        if 'password1' in self.fields:
            self.fields['password1'].help_text = ''
        if 'password2' in self.fields:
            self.fields['password2'].help_text = ''

        # Add CSS classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location', 'birth_date', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Tell us about yourself...',
                'maxlength': '500'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'City, Country',
                'maxlength': '30'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://yourwebsite.com',
                'maxlength': '200'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Check file size (max 2MB for avatars)
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Avatar file too large. Maximum size is 2MB.")
            
            # Check file type
            if hasattr(avatar, 'content_type') and not avatar.content_type.startswith('image/'):
                raise forms.ValidationError("Please upload a valid image file.")
        
        return avatar

    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website and not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        return website


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': "What's on your mind?",
                'style': 'resize: none;',
                'maxlength': '2000'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('content'),
            Row(
                Column(Field('image'), css_class='form-group col-md-6 mb-0'),
                Column(Field('video'), css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Share Post', css_class='btn btn-primary w-100 mt-4')
        )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or not content.strip():
            raise forms.ValidationError("Post content cannot be empty.")
        if len(content.strip()) < 3:
            raise forms.ValidationError("Post content must be at least 3 characters long.")
        return content.strip()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large. Maximum size is 5MB.")
            
            # Check file type
            if hasattr(image, 'content_type') and not image.content_type.startswith('image/'):
                raise forms.ValidationError("Please upload a valid image file.")
        
        return image

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            # Check file size (max 20MB for videos)
            if video.size > 20 * 1024 * 1024:
                raise forms.ValidationError("Video file too large. Maximum size is 20MB.")
            
            # Check file type
            if hasattr(video, 'content_type') and not video.content_type.startswith('video/'):
                raise forms.ValidationError("Please upload a valid video file.")
        
        return video


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ReplyForm(forms.ModelForm):
    text = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Reply to this comment...',
                'class': 'form-control form-control-sm',
                'autocomplete': 'off',
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['text']