from django.db import models

# Create your models here.
from django.db import models

class Record(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    synced = models.BooleanField(default=False)  # Indicates if record was synced to read_db

    def __str__(self):
        return self.title

class SyncStatus(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    message = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Record {self.record.id} - {self.status}"