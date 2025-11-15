# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "bio"]

# edit profile
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname","bio", "profile_pic","sustainability_interests","venmo_handle","paypal_handle","other_payment_note",]