# Generated by Django 3.1 on 2025-04-29 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20201014_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Код товара'),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='Количество'),
        ),
    ]
