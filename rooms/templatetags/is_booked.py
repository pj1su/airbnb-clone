import datetime
from django import template
from reservations import models as reservation_models

# 템플릿태크로 필터를 만들 수 있다 {{something|sexy_capitals}}하면 value는 something 나오는 값은 return값
# 태그는 필터보다 더 많은 기능을 가질 수 있고 좋다

register = template.Library()

# @register.simple_tag(takes_context=True)-콘텍스트는 django가 전달해주는 user나 다른 context를 받을 수 있음 , register.tag도 가능 이게 더 기능이 많음
@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        reservation_models.BookedDay.objects.get(day=date, reservation__room=room)
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False