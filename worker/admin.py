from django.contrib import admin
from worker.models import worker_tracker

# Register your models here.
admin.site.register(worker_tracker)