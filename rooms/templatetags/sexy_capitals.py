from django import template

# 템플릿태크로 필터를 만들 수 있다 {{something|sexy_capitals}}하면 value는 something 나오는 값은 return값
# 태그는 필터보다 더 많은 기능을 가질 수 있고 좋다

register = template.Library()


@register.filter(name="sexy_capitals")
def randomvariable(value):
    # print(value)
    return "lalalalala"