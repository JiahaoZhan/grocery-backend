from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class List(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default="")    
    name = models.CharField(max_length=255, default="")
    color = models.CharField(max_length=255, default="")
    total = models.PositiveBigIntegerField(default=0)
    checked = models.PositiveBigIntegerField(default=0)
    description = models.CharField(max_length=255, default="", blank=True)
    complete = models.BooleanField(default = False)
    
class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default="")
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='products', default="")
    name = models.CharField(max_length=255, default="")
    note = models.CharField(max_length=255, default="", blank=True)
    quantity = models.PositiveBigIntegerField(default=0)
    checked = models.BooleanField(default = False)

class SharedList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default="")    
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='shared_list', default="")
    list_name = models.CharField(max_length=255, default="")
    access_token = models.CharField(max_length=255, default="")
    
