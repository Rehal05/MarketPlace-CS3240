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
        fields = [
            "nickname",
            "bio",
            "sustainability_interests",
            "venmo_handle",
            "paypal_handle",
            "other_payment_note",
        ]

        widgets = {
            "nickname": forms.TextInput(attrs={"maxlength": 50}),
            "bio": forms.Textarea(attrs={"maxlength": 500}),
            "sustainability_interests": forms.Textarea(attrs={"maxlength": 200}),
            "venmo_handle": forms.TextInput(attrs={"maxlength": 50}),
            "paypal_handle": forms.TextInput(attrs={"maxlength": 50}),
            "other_payment_note": forms.Textarea(attrs={"maxlength": 200}),
        }
