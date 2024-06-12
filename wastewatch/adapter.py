from django.contrib.auth.models import User

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

# automatically link social account to existing account if account with same email exists
class AutoConnect(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            return
        if not user.email:
            return

        try:
            user = User.objects.get(
                email=user.email)  # if user exists, connect the account to the existing account and login
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass