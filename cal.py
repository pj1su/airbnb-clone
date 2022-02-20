# python library도 사용가능 파일이름을 calender.py로 하면안됨 파이썬라이브러리 캘린더와 겹침
from django.utils import timezone
import calendar


class Calender(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)  # 1주마다 리스트로 나옴
        days = []
        for week in weeks:  # 1주 2주 3주  주로 리스트를 뽑아오고
            for day, _ in week:  # 1일 단위로 다 뽑아옴 (일,요일)
                now = timezone.now()
                today = now.day
                month = now.month
                past = False
                if month == self.month:
                    if day <= today:
                        past = True
                new_day = Day(number=day, past=past, month=self.month, year=self.year)
                days.append(new_day)
        return days

    def get_month(self):
        return self.months[self.month - 1]


class Day:
    def __init__(self, number, past, month, year):
        self.number = number
        self.past = past
        self.month = month
        self.year = year

    def __str__(self):
        return str(self.number)