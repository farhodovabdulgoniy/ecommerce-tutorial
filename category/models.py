from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    cat_image = models.ImageField(upload_to='photos/categories',blank=True)

    def __str__(self):
        return self.category_name
        
    def get_absolute_url(self):
        return reverse('products_by_category',args=[self.slug])#path of function on urls.py 

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'