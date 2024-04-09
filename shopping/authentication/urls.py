from django.urls import path
from .views import EmployeeSignup, EmployeeLogin, ProductCRUD, CustomerCRUD


urlpatterns = [
    path('signup', EmployeeSignup.as_view()),
    path('login', EmployeeLogin.as_view()),
    path('products', ProductCRUD, name='product_list_create'),
    path('products/<int:pk>', ProductCRUD, name='product_detail'),

    path('customers', CustomerCRUD, name='customer_list_create'),
    path('customers/<int:pk>', CustomerCRUD, name='customer_detail'),
]
