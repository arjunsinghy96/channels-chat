from django.contrib.auth.models import User

def sentient_user():
    return User.objects.get_or_create(username='default_user')[0]
