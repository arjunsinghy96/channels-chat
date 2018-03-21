from django.db import models
from django.contrib.auth.models import User

from my_messages.models import League

class Invite(models.Model):
    PERMISSIONS = (
        ('4', 'owner'),
        ('3', 'master'),
        ('2', 'member'),
        ('1', 'guest')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=1,
                                   choices=PERMISSIONS,
                                   default='2')
    
    class Meta:
        unique_together = ("user", "league",)