from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название банка")
    number_offices = models.IntegerField(blank=True, default=0, verbose_name="Количество офисов")
    number_atms = models.IntegerField(blank=True, default=0, verbose_name="Количество ATM")
    number_employees = models.IntegerField(blank=True, default=0, verbose_name="Количество сотрудников")
    number_clients = models.IntegerField(blank=True, default=0, verbose_name="Количество клиентов")
    rating = models.IntegerField(null=True, blank=True, verbose_name="Рейтинг")
    total_money = models.IntegerField(null=True, blank=True, verbose_name="Всего денег")
    interest_rate = models.FloatField(null=True, blank=True, verbose_name="Процентная ставка")


class BankOffice(models.Model):
    statuses = [
        ('work', 'работает'),
        ('not work', 'не работает')
    ]

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name="Банк")
    name = models.CharField(max_length=255, verbose_name="Название")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    status = models.CharField(max_length=255, choices=statuses, default='work', verbose_name="Статус")
    can_place_atm = models.BooleanField(verbose_name="Можно ли расположить автомат")
    num_atms = models.IntegerField(default=0, verbose_name="Количество автоматов")
    can_provide_credit = models.BooleanField(verbose_name="Может выдавать кредит")
    dispense_money = models.BooleanField(verbose_name="Работает на выдачу денег")
    accept_money = models.BooleanField(verbose_name="Можно ли внести деньги")
    money_in_office = models.IntegerField(null=True, blank=True, default=0, verbose_name="Денег в офисе")
    rent_cost = models.FloatField(verbose_name="Стоимость аренды банковского офиса")


class Employee(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name="Банк")
    bank_office = models.ForeignKey(BankOffice, on_delete=models.CASCADE, verbose_name="Офис банка")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    birth_date = models.DateField(verbose_name="Дата рождения")
    position = models.CharField(max_length=255, verbose_name="Должность")
    works_remotely = models.BooleanField(verbose_name="Работает удаленно")
    can_provide_credit = models.BooleanField(verbose_name="Может выдавать кредит")
    salary = models.FloatField(verbose_name="Зарплата")


class BankAtm(models.Model):
    statuses = [
        ('work', 'работает'),
        ('not work', 'не работает'),
        ('not money', 'нет денег')

    ]

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name="Банк")
    bank_office = models.ForeignKey(BankOffice, on_delete=models.CASCADE, verbose_name="Офис банка")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    name = models.CharField(max_length=255, verbose_name="Название")
    address = models.CharField(null=True, blank=True, max_length=255, verbose_name="Адрес")
    status = models.CharField(max_length=50, choices=statuses, default='work', verbose_name="Статус")
    dispense_money = models.BooleanField(verbose_name="Работает на выдачу денег")
    accept_money = models.BooleanField(verbose_name="Можно ли внести деньги")
    money_in_atm = models.IntegerField(null=True, blank=True, default=0, verbose_name="Денег в автомате")
    maintenance_cost = models.FloatField(verbose_name="Стоимость обслуживания")


class Client(models.Model):
    banks = models.ManyToManyField(Bank, verbose_name="Банки")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    birth_date = models.DateField(verbose_name="Дата рождения")
    job = models.CharField(max_length=255, verbose_name="Место работы")
    monthly_income = models.FloatField(verbose_name="Месячная зарплата")
    credit_rating = models.IntegerField(null=True, blank=True, verbose_name="Кредитный рейтинг")


class PaymentAccount(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    bank_name = models.CharField(max_length=255, verbose_name="Название банка")
    balance = models.FloatField(verbose_name="Баланс")


class CreditAccount(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    payment_account = models.ForeignKey(PaymentAccount, on_delete=models.CASCADE, verbose_name="Платежный аккаунт")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    bank_name = models.CharField(max_length=255, verbose_name="Название банка")
    start_date = models.DateField(auto_now_add=True, verbose_name="Дата начала кредита")
    end_date = models.DateField(verbose_name="Дата окончания кредита")
    loan_duration_months = models.IntegerField(verbose_name="Продолжительность в месяцах")
    loan_amount = models.FloatField(verbose_name="Сумма кредита")
    monthly_payment = models.FloatField(verbose_name="Ежемесячный платеж")
    interest_rate = models.FloatField(null=True, blank=True, verbose_name="Процентная ставка")
