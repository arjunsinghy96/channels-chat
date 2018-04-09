from django.db import models
from django.contrib.auth.models import User

from my_messages.models import League

class Membership(models.Model):
    PERMISSIONS = (
        ('4', 'owner'),
        ('3', 'master'),
        ('2', 'member'),
        ('1', 'guest')
    )
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=1,
                                   choices=PERMISSIONS,
                                   default='2')
    joined_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} in {}'.format(self.user, self.league)
    
    def can_send(self):
        return self.permissions != 'guest'