from rest_framework import serializers
from .models import Medicine, Category, StatusMedicines


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    medicines = MedicineSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class StatuMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusMedicines
        fields = '__all__'
