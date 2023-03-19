from django.db import models
import uuid
from category.models import Category


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=100.0)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
