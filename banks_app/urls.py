from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'banks', BankViewSet, basename='banks')
router.register(r'banks-offices', BankOfficeViewSet, basename='banks-offices')
router.register(r'employee', EmployeeViewSet, basename='employee')
router.register(r'banks-atm', BankAtmViewSet, basename='banks-atm')
router.register(r'client', ClientViewSet, basename='client')
router.register(r'payment-account', PaymentAccountViewSet, basename='payment-account')
router.register(r'credit-account', CreditAccountViewSet, basename='credit-account')


urlpatterns = [
    path('', include(router.urls)),
]
