import datetime as dt


class Record:
    date_now = dt.datetime.now().strftime('%d.%m.%Y')

    def __init__(self, amount, comment, date=date_now):
        self.amount = amount
        self.comment = comment
        self.date = date

    def __str__(self):
        return f"amount: {self.amount}, comment: {self.comment}, date: {self.date}"


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.total_day = 0
        self.total_week = 0
        self.date_format = '%d.%m.%Y'

    def add_record(self, record):
        """Сохраняет новую запись"""
        self.records.append(record)

    def get_current_day(self):
        """Возвращает текущий день"""
        now = dt.datetime.now()
        current_day = now.date()
        return current_day

    def get_day(self, record_date):
        """Возвращает день в записи"""
        moment = dt.datetime.strptime(record_date, self.date_format)
        day = moment.date()
        return day

    def get_today_stats(self):
        """Считает, сколько калорий съедено (денег потрачено) за сегодня"""
        return f"Сегодня Вы потратили: {self.total_day} "

    def get_week_stats(self):
        """Считает, сколько получено калорий (потрачено денег) за последние 7 дней"""
        for record in self.records:
            day = self.get_day(record.date)
            last_day = (self.get_current_day() - day).days

            if last_day < 7:
                self.total_week += record.amount

        return f"За неделю: {self.total_week}"

    def __str__(self):
        return f"limit: {self.limit}, records: {self.records}"


class CashCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)
        self.USD_RATE = 77.00
        self.EURO_RATE = 91.40

    def get_today_cash_remained(self, currency):
        """Баланс"""
        for record in self.records:
            day = self.get_day(record.date)

            if day == self.get_current_day():
                self.total_day += record.amount

        if currency == "eur":
            balance = (self.limit - self.total_day) / self.EURO_RATE
        elif currency == "usd":
            balance = (self.limit - self.total_day) / self.USD_RATE
        else:
            balance = self.limit - self.total_day

        if self.total_day > self.limit:
            return f"Денег нет, держись: твой долг - N {currency}"
        elif self.total_day == self.limit:
            return "Денег нет, держись"
        else:
            return f"На сегодня осталось {balance} {currency}"


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        """Определяет, сколько ещё калорий можно/нужно получить сегодня"""
        for record in self.records:
            day = self.get_day(record.date)

            if day == self.get_current_day():
                self.total_day += record.amount

        balance = self.limit - self.total_day

        if self.total_day > self.limit:
            return "Хватит есть"
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
r5 = Record(amount=84, comment='Йогурт.', date='23.02.2019')
r6 = Record(amount=1140, comment='Баночка чипсов.', date='08.04.2021')
r7 = Record(amount=1, comment='Сухарики.', date='02.04.2021')
r8 = Record(amount=1, comment='Хлеб.')



cash_calculator = CashCalculator(1000)
cash_calculator.add_record(r1)
cash_calculator.add_record(r3)
cash_calculator.add_record(r8)
print(cash_calculator.get_today_cash_remained("rub"))
print(cash_calculator.get_today_stats())
print(cash_calculator.get_week_stats())


# calories_calculator = CaloriesCalculator(2000)
# calories_calculator.add_record(r5)
# calories_calculator.add_record(r6)
# calories_calculator.add_record(r7)
# print(calories_calculator.get_calories_remained())
# print(calories_calculator.get_today_stats())
# print(calories_calculator.get_week_stats())


