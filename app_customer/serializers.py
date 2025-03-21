from rest_framework import serializers
from .models import Customer

class CustomerMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'message', 'created_at']
