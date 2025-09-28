from django.db import models


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_full_name = models.CharField(max_length=100)
    user_username = models.CharField(max_length=150, unique=False)
    user_email = models.EmailField(unique=True)
    user_phone = models.CharField(max_length=15, blank=True, unique=True, null=True)
    user_password = models.CharField(max_length=128)
    user_address = models.TextField(blank=True, null=True)
    user_city = models.CharField(max_length=100, blank=True, null=True)
    user_state = models.CharField(max_length=100, blank=True, null=True)
    user_zipcode = models.CharField(max_length=20, blank=True, null=True)
    user_country = models.CharField(max_length=100, blank=True, null=True)
    user_about = models.TextField(blank=True, null=True)
    user_type = models.CharField(max_length=50)
    user_is_active = models.BooleanField(default=True)
    user_profile = models.CharField(max_length=100, blank=True, null=True)
    user_profile_pic = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.user_id}"

class Contact_lead(models.Model):
    lead_id = models.AutoField(primary_key=True)
    lead_name = models.CharField(max_length=100)
    lead_email = models.EmailField()
    lead_phone = models.CharField(max_length=15)
    lead_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lead_name