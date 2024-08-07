from datetime import date

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    company = models.CharField(max_length=100)
    expire_date = models.DateField(default=date.today)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='medicines')

    def __str__(self):
        return f"{self.name} - {self.description}"


class StatusMedicines(models.Model):
    quantity = models.IntegerField()
    expire_date = models.DateField(default=date.today)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='medicines')

    def __str__(self):
        return f"{self.quantity} - {self.expire_date}-{self.medicine}"
