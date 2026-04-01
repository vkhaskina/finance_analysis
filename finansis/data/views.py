from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError, transaction
from .models import Share

import csv
from datetime import datetime

from .serializers import ShareSerializer


# Create your views here.
@api_view(['POST'])
@csrf_exempt
@transaction.atomic
def read_input(request):
    csv_file = request.FILES.get('csv_file')

    if not csv_file:
        return Response({
            "status": "error",
            "message": "Файл не был загружен"
        },
            status=400)

    if not csv_file.name.endswith('.csv'):
        return Response({
            "status": "error",
            "message": "Пожалуйста, загрузите CSV-файл"
        },
            status=400)

    try:
        decoded_csv = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_csv, delimiter=';')

        shares_to_create = []
        shares_errors = []

        with transaction.atomic():
            next(reader, None)
            for row_num, row  in enumerate(reader, start=2):

                print(row)

                cur_ticker = row[0].strip()
                str_date = row[2].strip()
                cur_open = row[4].strip().replace(',', '.')
                cur_high = row[5].strip().replace(',', '.')
                cur_low = row[6].strip().replace(',', '.')
                cur_close = row[7].strip().replace(',', '.')
                cur_vol = row[8].strip()

                try:
                    date_object = datetime.strptime(str_date, '%y%m%d')
                    cur_date = date_object.strftime('%Y-%m-%d')
                except ValueError:
                    shares_errors.append({
                        'row': row_num,
                        'error': f"Неверный формат даты"
                    })

                db_data = {
                    'filename': csv_file.name,
                    'ticker': cur_ticker,
                    'date': cur_date,
                    'open': cur_open,
                    'high': cur_high,
                    'low': cur_low,
                    'close': cur_close,
                    'vol': cur_vol
                }


                serializer = ShareSerializer(data=db_data)
                if serializer.is_valid():
                    shares_to_create.append((Share(**serializer.validated_data)))
                else:
                    shares_errors.append({
                        'row': row_num,
                        'error': serializer.errors
                    })

            if shares_errors:
                return Response({
                    "status": "error",
                    "message": "Некоторые строки не прошли валидацию",
                },
                    status=400
                )

            Share.objects.bulk_create(shares_to_create)

            return Response({
                "success": True,
                "message": f"Загружено {len(shares_to_create)} записей",
            },
                status=200
            )


    except UnicodeDecodeError:
        return Response({
            "status": "error",
            "message": "Ошибка в кодировке файла",
            },
            status=400
        )
    except IntegrityError:
        return Response({
            "status": "error",
            "message": f"Ошибка записи в БД",
        },
            status=400
        )
    except Exception as e:
        return Response({
            "status": "error",
            "message": f"Ошибка обработки csv: {str(e)}",
        },
            status=400
        )
