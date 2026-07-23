from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    reading_pace = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Fast, Moderate, 1 book/month")
    #favorite_genre = models.CharField(max_length=100, blank=True)
    #date_of_birth = models.DateField(null=True, blank=True)
    #profile_picture = models.ImageField(upload_image='profiles/', blank=True)
    
    # We will build out favorite genres and the 'bookshelf' later 
    # when we create the Books app and can link the tables together.

    def __str__(self):
        return self.username