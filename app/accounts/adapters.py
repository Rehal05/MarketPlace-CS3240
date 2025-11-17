from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse

class MyAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        return '/dashboard/'

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        return True

    def pre_social_login(self, request, sociallogin):
        # get email and  picture from Google
        if sociallogin.account.provider == 'google':
            email = sociallogin.account.extra_data.get('email')
            picture = sociallogin.account.extra_data.get('picture')
            if email:
                request.session['social_email'] = email
            if picture:
                request.session['social_picture'] = picture

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        # Save the profile picture URL
        if sociallogin.account.provider == 'google':
            picture = sociallogin.account.extra_data.get('picture')
            if picture:
                user.profile_pic = picture
            # Populate nickname with Google full name when the nickname is empty.
            if not user.nickname:
                full_name = sociallogin.account.extra_data.get('name')

                if full_name:
                    user.nickname = full_name.strip()[:50]
        
        return user
    
    def get_signup_redirect_url(self, request, sociallogin):
        # Redirect to dashboard after google auth
        return '/dashboard/'