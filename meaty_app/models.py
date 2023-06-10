from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    usia = models.IntegerField(null=True)
    domisili = models.CharField(max_length=100)
    pekerjaan = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
     
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='meat_users'  # Add a related_name argument here
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='meat_users'  # Add a related_name argument here
    )

class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploaded_images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=255)
    notes = models.TextField(null=True)

    def __str__(self):
        return str(self.image)

