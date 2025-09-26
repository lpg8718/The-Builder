from django.db import models


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_full_name = models.CharField(max_length=100)
    user_username = models.CharField(max_length=150, unique=False)
    user_email = models.EmailField(unique=True)
    user_phone = models.CharField(max_length=15, blank=True, unique=True, null=True)
    user_password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=50)
    user_is_active = models.BooleanField(default=True)
    user_profile = models.CharField(max_length=100, blank=True, null=True)
    user_profile_pic = models.ImageField(upload_to="profiles/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.user_username
