# social_app/forms.py

from django import forms
from social_app.models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label='',  # Removes the "Text:" label
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Add a comment...',
                'class': 'form-control',  # Adds styling support for Bootstrap/crispy-forms
                'autocomplete': 'off',
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['text']  # Only expose the text field

# social_app/forms.py (Corrected)

from django.contrib.auth.forms import UserCreationForm

# social_app/forms.py (Updated to clear username help text)

from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        pass
    
    # FIX: Override the help_text for password and username fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 🌟 Clears help text for the username field 🌟
        if 'username' in self.fields:
            self.fields['username'].help_text = ''
        
        # Clears help text for password fields (as done previously)
        if 'password1' in self.fields:
            self.fields['password1'].help_text = ''
        if 'password2' in self.fields:
            self.fields['password2'].help_text = ''