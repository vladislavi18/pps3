from rest_framework import serializers

from banks_app.models import Bank, BankOffice, Employee, BankAtm, Client, PaymentAccount, CreditAccount


class BankCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ('id', 'name',)


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = "__all__"


class BankOfficeSerializer(serializers.ModelSerializer):
    bank = serializers.SlugRelatedField(queryset=Bank.objects.all(), slug_field='name')

    class Meta:
        model = BankOffice
        fields = (
            'id', 'bank', 'name', 'address', 'status', 'can_place_atm', 'can_provide_credit', 'dispense_money',
            'accept_money', 'rent_cost'
        )

    # def to_representation(self, instance):
    #     # Переопределяем представление объекта
    #     representation = super().to_representation(instance)
    #     representation['bank'] = instance.bank.name
    #     print(representation)
    #     return representation


class EmployeeSerializer(serializers.ModelSerializer):
    bank = serializers.SlugRelatedField(queryset=Bank.objects.all(), slug_field='name')
    bank_office = serializers.SlugRelatedField(queryset=BankOffice.objects.all(), slug_field='name')

    class Meta:
        model = Employee
        fields = '__all__'


class BankAtmSerializer(serializers.ModelSerializer):
    bank = serializers.SlugRelatedField(queryset=Bank.objects.all(), slug_field='name')
    bank_office = serializers.SlugRelatedField(queryset=BankOffice.objects.all(), slug_field='name')

    class Meta:
        model = BankAtm
        fields = (
            'id', 'bank', 'bank_office', 'employee', 'name', 'status', 'dispense_money', 'accept_money',
            'maintenance_cost')


class ClientSerializer(serializers.ModelSerializer):
    banks = serializers.SlugRelatedField(queryset=Bank.objects.all(), slug_field='name', many=True)

    class Meta:
        model = Client
        fields = ('id', 'banks', 'full_name', 'birth_date', 'job', 'monthly_income')


class PaymentAccountSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='full_name')

    class Meta:
        model = PaymentAccount
        fields = '__all__'


class CreditAccountSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='full_name')

    class Meta:
        model = CreditAccount
        fields = (
            'id', 'employee', 'payment_account', 'client', 'bank_name', 'start_date', 'end_date', 'loan_duration_months',
            'loan_amount', 'monthly_payment')


class CreateCreditAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditAccount
        fields = (
            'id', 'employee', 'payment_account', 'client', 'bank_name', 'end_date',
            'loan_amount', 'monthly_payment')
