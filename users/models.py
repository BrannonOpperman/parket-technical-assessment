from django.db import models

class ParketUser(models.Model):
    """User model for the parking system"""
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField('Email address')
    license_plate = models.CharField(max_length=20)
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='parket_users'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['email', 'client']
        verbose_name = 'Parket User'
        verbose_name_plural = 'Parket Users'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - ({self.license_plate})"
