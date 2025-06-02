from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('movie', 'Фильм'),
        ('subscription', 'Подписка'),
        ('merch', 'Мерч'),
        ('bonus', 'Бонусные материалы'),
    ]

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='media/products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    currency = models.CharField(
        max_length=10,
        default="RUB",
        choices=[("RUB", "₽"), ("USD", "$"), ("EURO", "€")],
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_price(self):
        return self.price * Decimal(100 - self.discount) / Decimal(100)
