from django.db import models

# Create your models here.

class worker_tracker(models.Model):
    id = models.IntegerField(primary_key=True)
    file_or_dir_name = models.CharField(max_length=240)
    updated_at = models.DateTimeField(auto_now=True)
    updating = models.BooleanField(default=False)

    def __str__(self):
        return str(self.file_or_dir_name)

    