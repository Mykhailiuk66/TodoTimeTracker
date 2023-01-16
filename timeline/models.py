from django.db import models
from users.models import Profile
import uuid
# Create your models here.


class Timeline(models.Model):
    COLORS = (
        ('#0000FF', 'Blue'),
        ('#FF0000', 'Red'),
        ('#FFFF00', 'Yellow'),
        ('#00FF00', 'Lime'),
        ('#800000', 'Maroon'),
        ('#008000', 'Green'),
        ('#00FFFF', 'Aqua'),
        ('#000080', 'Navy'),
        ('#800080', 'Purple'),
    ) 
    
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300, blank=False, null=False)
    color = models.CharField(max_length=200, choices=COLORS, default=COLORS[0][0], null=False, blank=False)
    active = models.BooleanField(default=False, null=False, blank=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.title)
        
    
    
class Record(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    @property
    def period(self):
        lasted = self.end_time - self.start_time
        return lasted
    
    @property
    def periodSeconds(self):
        lasted = self.end_time - self.start_time
        lasted = lasted.total_seconds()
        return lasted
    
    
    def __str__(self):
        return f"{self.timeline.title} - Record - {self.id}"
    
    class Meta:
        ordering = ['start_time']
    
    