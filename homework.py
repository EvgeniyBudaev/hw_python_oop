import datetime as dt
from decimal import Decimal


class Record:
    def __init__(self, amount, comment, date=dt.datetime.now().date()):
        self.amount = amount
        self.comment = comment
        self.date = None
        self.is_date(date)

    def is_date(self, date):
        """Проверка на вхождение date"""
        if isinstance(date, str):
            date_format = '%d.%m.%Y'
            moment = dt.datetime.strptime(date, date_format)
            day = moment.date()
            self.date = day
        else:
            self.date = date


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.total_day = 0
        self.total_week = 0
        self.today = dt.date.today()
        self.week_ago = self.today - dt.timedelta(7)

    def add_record(self, record):
        """Сохраняет новую запись"""
        self.records.append(record)

    def get_current_day(self):
        """Возвращает текущий день"""
        now = dt.datetime.now()
        current_day = now.date()
        return current_day

    def get_today_stats(self):
        """Считает, сколько калорий съедено (денег потрачено)
         за сегодня"""
        for record in self.records:
            if record.date == self.get_current_day():
                self.total_day += record.amount
        result = self.rounding(self.total_day)
        return result

    def get_week_stats(self):
        """Считает, сколько получено калорий (потрачено денег)
         за последние 7 дней"""
        for record in self.records:
            if self.week_ago <= record.date <= self.today:
                self.total_week += record.amount
        result = self.rounding(self.total_week)
        return result

    def get_today_balance(self):
        """Получение баланса за сегодня"""
        balance = self.limit - self.get_today_stats()
        return balance

    def rounding(self, num):
        """Округляет до второго знака после запятой"""
        number = Decimal(num)
        number = number.quantize(Decimal("1.00"))
        return number


class CashCalculator(Calculator):
    EURO_RATE = 91.40
    USD_RATE = 77.00
    RUB_RATE = 1

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency="rub"):
        """Баланс"""
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}

        get_balance = self.get_today_balance()

        if get_balance == 0:
            return 'Денег нет, держись'
        if currency not in currencies:
            return f'Валюты {currency} такой нет'
        name, rate = currencies[currency]
        get_balance = round(get_balance / rate, 2)
        if get_balance > 0:
            message = f'На сегодня осталось {get_balance} {name}'
        else:
            get_balance_abs = abs(get_balance)
            message = (f'Денег нет, держись: твой долг - {get_balance_abs} '
                       f'{name}')
        return message


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        """Определяет, сколько ещё калорий можно/нужно получить сегодня"""
        for record in self.records:
            day = record.date

            if day == self.get_current_day():
                self.total_day += record.amount

        balance = self.limit - self.total_day

        if self.total_day > self.limit:
            return "Хватит есть!"
        else:
            message = (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                       f'калорийностью не более {balance} кКал')
            return message
