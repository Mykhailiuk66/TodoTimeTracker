from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    profile_img = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    

    def __str__(self) :
        return str(self.user.username)
    
    
    @property
    def imageURL(self):
        try:
            url = self.profile_img.url
        except:
            url = ''
        return url