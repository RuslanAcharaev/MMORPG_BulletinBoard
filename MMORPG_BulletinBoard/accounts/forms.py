from django.conf import settings
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail
import random


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        user.is_active = False
        confirmation_code = ''.join(random.choice('0123456789') for _ in range(6))
        user.code = confirmation_code
        user.save()

        common_users = Group.objects.get(name='common users')
        user.groups.add(common_users)

        send_mail(
            subject='Код подтверждения регистрации',
            message=f'Ваш код подтверждения регистрации: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )

        return user
