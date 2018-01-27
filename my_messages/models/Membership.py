from django.db import models
from django.contrib.auth.models import User

from my_messages.models import League

class Membership(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} in {}'.format(self.user, self.league)
