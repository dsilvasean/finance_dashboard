from django.db import models

# Create your models here.

class worker_tracker(models.Model):
    id = models.IntegerField(primary_key=True)
    instance = models.CharField(max_length=100)
    started_at = models.DateTimeField(auto_now=True)
    running_status = models.BooleanField()

    