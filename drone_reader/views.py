from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import QRCodeData
from main.models import Product, StorageItem
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# Create your views here.

@csrf_exempt
@require_POST
def receive_qr_data(request):
    try:
        data = json.loads(request.body)
        qr_data = data.get('qr_data')
        
        if not qr_data:
            return JsonResponse({'error': 'No QR data provided'}, status=400)
        
        logger.info(f"Received QR data: {qr_data}")
        
        # Парсим данные QR-кода (формат: "стоимость за единицу, наименование, количество")
        try:
            # Разделяем строку по запятым и убираем пробелы
            parts = [part.strip() for part in qr_data.split(',')]
            
            if len(parts) != 3:
                logger.error(f"Invalid QR format. Got {len(parts)} parts instead of 3")
                return JsonResponse({
                    'error': 'Invalid QR format. Expected: price per unit, title, quantity'
                }, status=400)
            
            price, title, quantity = parts
            
            # Преобразуем значения в нужные типы данных
            try:
                price = Decimal(price)
                if price <= 0:
                    logger.error("Price must be greater than 0")
                    return JsonResponse({
                        'error': 'Price per unit must be greater than 0'
                    }, status=400)
                    
                quantity = int(quantity)
                if quantity <= 0:
                    logger.error("Quantity must be greater than 0")
                    return JsonResponse({
                        'error': 'Quantity must be greater than 0'
                    }, status=400)
            except (ValueError, TypeError) as e:
                logger.error(f"Error converting values: {str(e)}")
                return JsonResponse({
                    'error': f'Invalid number format: {str(e)}'
                }, status=400)
            
            # Создаем запись в базе данных
            qr_record = QRCodeData.objects.create(
                qr_data=qr_data,
                title=title,
                price=price,
                quantity=quantity
            )
            
            # Создаем или обновляем запись в StorageItem
            if qr_record.product:
                storage_item, created = StorageItem.objects.get_or_create(
                    product=qr_record.product,
                    defaults={'count': quantity}
                )
                if not created:
                    storage_item.count += quantity
                    storage_item.save()
            
            logger.info(f"Successfully created QR record with ID: {qr_record.id}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'QR data received and processed',
                'qr_id': qr_record.id,
                'product_id': qr_record.product.id if qr_record.product else None,
                'product_code': qr_record.code
            })
            
        except ValueError as e:
            logger.error(f"Value error: {str(e)}")
            return JsonResponse({
                'error': f'Invalid data format: {str(e)}'
            }, status=400)
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
