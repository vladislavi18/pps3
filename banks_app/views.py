import math
import random
from datetime import datetime

from django.shortcuts import render
from rest_framework import viewsets

from .models import Bank, BankAtm, BankOffice, Employee, Client, PaymentAccount, CreditAccount
from .serializers.serializers import BankSerializer, BankAtmSerializer, BankOfficeSerializer, EmployeeSerializer, \
    ClientSerializer, PaymentAccountSerializer, CreditAccountSerializer, BankCreateSerializer, \
    CreateCreditAccountSerializer


class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return BankCreateSerializer
        return BankSerializer

    def perform_create(self, serializer):
        rating = random.randint(0, 100)
        total_money = random.randint(0, 1000000)
        interest_rate = random.uniform(0, 20)

        if rating > 80:
            interest_rate *= 0.5
        elif rating > 60:
            interest_rate *= 0.7
        elif rating > 40:
            interest_rate *= 0.9

        serializer.save(total_money=total_money, interest_rate=round(interest_rate, 2), rating=rating)


class BankOfficeViewSet(viewsets.ModelViewSet):
    queryset = BankOffice.objects.all()
    serializer_class = BankOfficeSerializer

    def perform_create(self, serializer):
        bank_id = self.request.data.get('bank')
        bank = Bank.objects.get(id=bank_id)

        bank.number_offices += 1
        bank.save()

        serializer.save(money_in_office=bank.total_money)

    def perform_destroy(self, instance):
        bank = Bank.objects.get(id=instance.bank.id)

        bank.number_offices -= 1
        bank.save()
        instance.delete()


class BankAtmViewSet(viewsets.ModelViewSet):
    queryset = BankAtm.objects.all()
    serializer_class = BankAtmSerializer

    def perform_create(self, serializer):
        bank_office_id = self.request.data.get('bank_office')
        bank_office = BankOffice.objects.get(id=bank_office_id)
        bank_id = self.request.data.get('bank')
        bank = Bank.objects.get(id=bank_id)

        bank.number_atms += 1
        bank.save()
        bank_office.num_atms += 1
        bank_office.save()

        serializer.save(address=bank_office.address, money_in_atm=bank.total_money)

    def perform_destroy(self, instance):
        bank_office = BankOffice.objects.get(id=instance.bank_office.id)
        bank = Bank.objects.get(id=instance.bank.id)

        bank.number_atms -= 1
        bank.save()
        bank_office.num_atms -= 1
        bank_office.save()
        instance.delete()


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        bank_id = self.request.data.get('bank')
        bank = Bank.objects.get(id=bank_id)
        bank.number_employees += 1
        bank.save()

        serializer.save()

    def perform_destroy(self, instance):
        bank = Bank.objects.get(id=instance.bank.id)
        bank.number_employees -= 1
        bank.save()
        instance.delete()


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        monthly_income = self.request.data.get('monthly_income')
        credit_rating = math.ceil(monthly_income / 1000) * 100
        banks = self.request.data.get('banks')

        for bank in banks:
            bank = Bank.objects.get(id=bank)
            bank.number_clients += 1
            bank.save()

        serializer.save(credit_rating=credit_rating)

    def perform_destroy(self, instance):
        banks = instance.banks.all()

        for bank in banks:
            bank = Bank.objects.get(id=bank.id)
            bank.number_clients -= 1
            bank.save()

        instance.delete()


class PaymentAccountViewSet(viewsets.ModelViewSet):
    queryset = PaymentAccount.objects.all()
    serializer_class = PaymentAccountSerializer


class CreditAccountViewSet(viewsets.ModelViewSet):
    queryset = CreditAccount.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCreditAccountSerializer
        return CreditAccountSerializer

    def perform_create(self, serializer):
        bank_name = self.request.data.get('bank_name')
        bank = Bank.objects.get(name=bank_name)
        start_date = datetime.now().date()
        end_date = serializer.validated_data.get('end_date')

        loan_duration_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

        serializer.save(interest_rate=round(bank.interest_rate, 2), loan_duration_months=loan_duration_months)
