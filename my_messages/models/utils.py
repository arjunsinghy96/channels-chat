from django.contrib.auth.models import User

def sentient_user():
    return User.objects.get_or_create(username='default_user')[0]

def verify_username(username):
    """
    Check if a username is valid and available.
    """
    if len(username)<3 or len(username)>150:
        return {'error': 'Username should at least be 3 characters long'}
    else:
        try:
            int(username)
            return {'error': 'Username cannot be an integer'}
        except ValueError:
            try:
                float(username)
                return {'error': 'Username cannot be a number'}
            except ValueError:
                return True
