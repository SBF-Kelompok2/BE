from django.db import models
import uuid

from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userdata")
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Data"


class ProductEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # tambahkan baris ini
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_desc = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.product_name} by {self.user.username}"

"""
keranjang:
fk user
fk keanjanh

"""