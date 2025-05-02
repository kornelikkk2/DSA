from django.db import models
from main.models import Product
import uuid

# Create your models here.

class QRCodeData(models.Model):
    qr_data = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    is_processed = models.BooleanField(default=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"QR Code: {self.qr_data} at {self.timestamp}"

    def save(self, *args, **kwargs):
        if self.qr_data and not self.product:
            # Генерируем уникальный код товара
            generated_code = str(uuid.uuid4().hex)[:8].upper()
            
            # Создаем новый продукт
            self.product = Product.objects.create(
                title=self.title,
                code=generated_code,
                quantity=self.quantity,
                price=self.price
            )
            self.code = generated_code
            self.is_processed = True
            
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']
