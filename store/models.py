from django.db import models
from django.urls import reverse
from category.models import Category

# Create your models here.
class Product(models.Model):
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='category/images/')
    stock = models.IntegerField()

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('products_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    
