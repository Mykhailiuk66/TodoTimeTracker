import uuid
from django.db import models
from users.models import Profile

class Task(models.Model):
    PRIORITY = (
        (1, 'Low'),
        (2, 'Middle'),
        (3, 'High'),
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)    
    title = models.CharField(verbose_name="Task", max_length=200, blank=False)
    note = models.TextField(max_length=300 ,null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    priority = models.SmallIntegerField(choices=PRIORITY)
    done = models.BooleanField(null=False, blank=False, default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True ,unique=True, editable=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['done', '-priority', '-created']
    
    

class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
