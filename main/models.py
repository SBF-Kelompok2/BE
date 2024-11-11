from django.db import models
import uuid

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# class MoodEntry(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # tambahkan baris ini
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     mood = models.CharField(max_length=255)
#     time = models.DateField(auto_now_add=True)
#     feelings = models.TextField()
#     mood_intensity = models.IntegerField()

#     @property
#     def is_mood_strong(self):
#         return self.mood_intensity > 5
    
class ProductEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # tambahkan baris ini
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_desc = models.TextField()
    price = models.IntegerField()