from django.db import models

class Details(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    amount=models.CharField(max_length=100)
    payment_id=models.CharField(max_length=100)
    paid=models.BooleanField(default=False) 
