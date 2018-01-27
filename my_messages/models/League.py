from django.db import models
from django.contrib.auth.models import User


class League(models.Model):
    """
    Corresponds to room/group
    """
    name = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(User,
                                     through='Membership',
                                     related_name='member_of')

    def __str__(self):
        return self.name
