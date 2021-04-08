import datetime as dt
from decimal import Decimal


class Record:
    def __init__(self, amount, comment, date=dt.datetime.now().date()):
        self.amount = amount
        self.comment = comment
        self.date = None
        self.is_date(date)

    def is_date(self, date):
        if isinstance(date, str):
            date_format = '%d.%m.%Y'
            moment = dt.datetime.strptime(date, date_format)
            day = moment.date()
            self.date = day
        else:
            self.date = date

    def __str__(self):
        return f"amount: {self.amount}, comment: {self.comment}, date: {self.date}"


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.total_day = 0
        self.total_week = 0
        self.total_all_time = 0

    def add_record(self, record):
        """Сохраняет новую запись"""
        self.records.append(record)

    def get_current_day(self):
        """Возвращает текущий день"""
        now = dt.datetime.now()
        current_day = now.date()
        return current_day

    def get_today_stats(self):
        """Считает, сколько калорий съедено (денег потрачено) за сегодня"""
        result = self.rounding(self.total_day)
        return f"Сегодня Вы потратили: {result}"

    def get_week_stats(self):
        """Считает, сколько получено калорий (потрачено денег) за последние 7 дней"""
        for record in self.records:
            last_day = (self.get_current_day() - record.date).days

            if last_day < 7:
                self.total_week += record.amount

        result = self.rounding(self.total_week)
        return f"За неделю: {result}"

    def get_all_time(self):
        """Считает, сколько потрачено за всё время"""

        for record in self.records:
            last_day = (self.get_current_day() - record.date).days

            if last_day < 7:
                self.total_day += record.amount

        result = self.rounding(self.total_day)
        return f"За всё время: {result}"

    def rounding(self, num):
        number = Decimal(num)
        number = number.quantize(Decimal("1.00"))
        return number

    def __str__(self):
        return f"limit: {self.limit}, records: {self.records}"


class CashCalculator(Calculator):
    EURO_RATE = 91.40
    USD_RATE = 77.00
    balance = 0

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        """Баланс"""
        for record in self.records:
            day = record.date

            if day == self.get_current_day():
                self.total_day += record.amount
                self.total_all_time += record.amount
            else:
                self.total_all_time += record.amount

        if currency == "Euro":
            difference = (self.limit - self.total_day) / self.EURO_RATE
            self.balance = self.rounding(difference)
        elif currency == "USD":
            difference = (self.limit - self.total_day) / self.USD_RATE
            self.balance = self.rounding(difference)
        elif currency == "руб":
            difference = self.limit - self.total_day
            self.balance = self.rounding(difference)

        if self.total_day > self.limit:
            return f"Денег нет, держись: твой долг - {abs(self.balance)} {currency}"
        elif self.total_day == self.limit:
            return "Денег нет, держись"
        else:
            return f"На сегодня осталось {self.balance} {currency}"


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
            return f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {balance} кКал"



# для CashCalculator
r1 = Record(amount=145, comment='Безудержный шопинг', date='02.04.2021')
r2 = Record(amount=1568,
            comment='Наполнение потребительской корзины',
            date='08.04.2021')
r3 = Record(amount=690, comment='Катание на такси', date='08.04.2021')

# для CaloriesCalculator
r4 = Record(amount=1186,
            comment='Кусок тортика. И ещё один.',
            date='24.02.2019')
r5 = Record(amount=100, comment='Йогурт.', date='23.02.2019')
r6 = Record(amount=1140, comment='Баночка чипсов.', date='08.04.2021')
r7 = Record(amount=1, comment='Сухарики.', date='02.04.2021')
r8 = Record(amount=1, comment='Хлеб.')
r9 = Record(amount=1000, comment='Сковородка')
r10 = Record(amount=499.9999, comment='Ноутбук')
r11 = Record(amount=0, comment='Пусто')



cash_calculator = CashCalculator(1000)
# cash_calculator.add_record(r1)
# cash_calculator.add_record(r3)
# cash_calculator.add_record(r5)
cash_calculator.add_record(r7)
# cash_calculator.add_record(r8)
# cash_calculator.add_record(r9)
cash_calculator.add_record(r10)
# cash_calculator.add_record(r11)
print(cash_calculator.get_today_cash_remained("USD"))
print(cash_calculator.get_today_stats())
print(cash_calculator.get_week_stats())


# calories_calculator = CaloriesCalculator(2000)
# calories_calculator.add_record(r5)
# calories_calculator.add_record(r6)
# calories_calculator.add_record(r8)
# print(calories_calculator.get_calories_remained())
# print(calories_calculator.get_today_stats())
# print(calories_calculator.get_week_stats())


