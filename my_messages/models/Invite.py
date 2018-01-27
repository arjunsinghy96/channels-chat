from django.db import models
from django.contrib.auth.models import User

from my_messages.models import League

class Invite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
