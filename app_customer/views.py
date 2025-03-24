from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Customer
from .serializers import CustomerMessageSerializer

class CustomerMessage(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def post(self, request):
        serializer = CustomerMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Message sent successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            try:
                customer = Customer.objects.get(pk=pk)
                serializer = CustomerMessageSerializer(customer)
                return Response({"msg": "Customer fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            customers = Customer.objects.all()
            serializer = CustomerMessageSerializer(customers, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            customer.delete()
            return Response({"msg": "Customer deleted successfully"}, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
