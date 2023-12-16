from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to = 'imagenes_users')
    rol = models.CharField(max_length=10, choices=CHOICES, null=True, blank=True)

    def __str__(self):
        return 'User: '+ self.user.username + ', User Rol: ' + str(self.rol)