import datetime as dt


class Record:
    def __init__(self, amount, comment, date):
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
        """Сохраняет новую запись о приёме пищи"""
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


    def __str__(self):
        return f"limit: {self.limit}, records: {self.records}"


class CashCalculator(Calculator):
    def get_today_cash_remained(self, currency):
        pass


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)


    def get_calories_remained(self):
        """Определяет, сколько ещё калорий можно/нужно получить сегодня """
        for record in self.records:
            day = self.get_day(record.date)

            if day == self.get_current_day():
                self.total_day += record.amount

        balance = self.limit - self.total_day

        if self.total_day > self.limit:
            print("Хватит есть")
        else:
            print(f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {balance} кКал")


    def get_today_stats(self):
        """Считает, сколько калорий уже съедено сегодня"""
        print(f"Сегодня Вы съели калорий: {self.total_day} ")


    def get_week_stats(self):
        """Считает, сколько калорий получено за последние 7 дней"""
        for record in self.records:
            day = self.get_day(record.date)
            last_day = (self.get_current_day() - day).days

            if last_day < 7:
                self.total_week += record.amount

        print(f"total_week: {self.total_week}")


# для CashCalculator
r1 = Record(amount=145, comment='Безудержный шопинг', date='08.03.2019')
r2 = Record(amount=1568,
            comment='Наполнение потребительской корзины',
            date='09.03.2019')
r3 = Record(amount=691, comment='Катание на такси', date='08.03.2019')

# для CaloriesCalculator
r4 = Record(amount=1186,
            comment='Кусок тортика. И ещё один.',
            date='24.02.2019')
r5 = Record(amount=84, comment='Йогурт.', date='23.02.2019')
r6 = Record(amount=1140, comment='Баночка чипсов.', date='01.04.2021')
r7 = Record(amount=1, comment='Сухарики.', date='07.04.2021')


# # создадим калькулятор денег с дневным лимитом 1000
# cash_calculator = CashCalculator(1000)
#
# # а тут пользователь указал дату, сохраняем её
# cash_calculator.add_record(Record(amount=3000,
#                                   comment='бар в Танин др',
#                                   date='08.11.2019'))


calories_calculator = CaloriesCalculator(2000)
calories_calculator.add_record(r5)
calories_calculator.add_record(r6)
calories_calculator.add_record(r7)
calories_calculator.get_calories_remained()
calories_calculator.get_today_stats()
calories_calculator.get_week_stats()


