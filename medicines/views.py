from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.decorators import supplier_required
from .models import Category, StatusMedicines
from .serializer import MedicineSerializer, CategorySerializer, StatuMedicineSerializer
from django.db import transaction
from .models import Medicine


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(request):
    medicine = Medicine.objects.all()
    serializer = MedicineSerializer(medicine, many=True)
    return Response({'medicine': serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getByID(request, pk):
    try:
        with transaction.atomic():
            medicine = Medicine.objects.get(pk=pk)
            serializer = MedicineSerializer(medicine)
            return Response({'medicine': serializer.data})

    except Medicine.DoesNotExist:
        return Response('NotFound', status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@supplier_required
def create(request):
    try:
        with transaction.atomic():
            quantity = request.data.get('quantity')
            expire_date = request.data.get('expire_date')

            if quantity is None or expire_date is None:
                return Response({'error': 'Quantity and expire_date are required.'}, status=status.HTTP_400_BAD_REQUEST)

            medicine_serializer = MedicineSerializer(data=request.data)

            if medicine_serializer.is_valid():
                medicine = medicine_serializer.save()

                status_medicine = StatusMedicines(
                    quantity=quantity,
                    expire_date=expire_date,
                    medicine=medicine
                )
                status_medicine.save()

                return Response({'medicine': medicine_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(medicine_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['put'])
@permission_classes([IsAuthenticated])
@supplier_required
def update(request, pk):
    try:
        with transaction.atomic():
            medicine = Medicine.objects.get(pk=pk)
            serializer = MedicineSerializer(medicine, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'medicine': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Medicine.DoesNotExist:
        return Response('NotFound', status=status.HTTP_404_NOT_FOUND) \

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['delete'])
@permission_classes([IsAuthenticated])
@supplier_required
def delete(request, pk):
    try:
        with transaction.atomic():
            medicine = Medicine.objects.get(pk=pk)
            medicine.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    except medicine.DoesNotExist:
        return Response('NotFound', status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def medicines_search_by_name(request, name):
    medicines = Medicine.objects.filter(name__icontains=name)
    if medicines.exists():
        return Response({'data': list(medicines.values()), 'message': 'Here is your search'})
    else:
        return Response({'data': [], 'message': 'No categories found'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@supplier_required
def createCategory(request):
    try:
        with transaction.atomic():
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'category': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_with_medicines(request, pk):
    try:
        category = Category.objects.prefetch_related('medicines').get(pk=pk)
        serializer = CategorySerializer(category)
        return Response({'category': serializer.data}, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_search_by_name(request, name):
    categories = Category.objects.filter(name__icontains=name)
    if categories.exists():
        return Response({'data': list(categories.values()), 'message': 'Here is your search'})
    else:
        return Response({'data': [], 'message': 'No categories found'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@supplier_required
def status_medicine_create(request):
    try:
        with transaction.atomic():
            serializer = StatuMedicineSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status_medicine': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
