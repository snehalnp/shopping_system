from django.shortcuts import render
from .serializers import EmployeeSerializer, ProductSerializer, CustomerSerializer, BillSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from .models import Employee, Product, Customer
import jwt
from datetime import timedelta, datetime
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.views import APIView

class EmployeeSignup(generics.CreateAPIView):
    serializer_class = EmployeeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail':'User Created Successfully!'}, status=status.HTTP_201_CREATED)
    
class EmployeeLogin(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = Employee.objects.filter(email=email).first()
        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token)
        response.data = {
            'jwt': token
        }
        return Response({'detail': 'Login successful!'}, status=status.HTTP_200_OK)
    


@api_view(['GET','POST','DELETE','PATCH'])
def ProductCRUD(request,pk=None):
    if request.method == 'POST' :
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)
    if request.method == "DELETE":
        Product.objects.filter(id=pk).delete()
        return JsonResponse({'message': 'Product was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    if request.method == "PATCH":
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product was updated successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET','POST','DELETE','PATCH'])
def CustomerCRUD(request,pk=None):
    if request.method == 'POST' :
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)
    if request.method == "DELETE":
        Customer.objects.filter(id=pk).delete()
        return JsonResponse({'message': 'Customer was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    if request.method == "PATCH":
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Customer was updated successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BillAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product']
            quantity_sold = serializer.validated_data['quantity_sold']
            product = Product.objects.get(pk=product_id)
            total_amount = product.price * quantity_sold
            
            serializer.save(total_amount=total_amount)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)