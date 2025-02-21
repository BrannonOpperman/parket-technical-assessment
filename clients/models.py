from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    administrators = models.ManyToManyField(
        User,
        blank=True,
        related_name='administered_clients',
        help_text="Users who can manage parket users for this client"
    )

    def __str__(self):
        return self.name
