from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    # print(context, room)
    # print(context.request)
    # print(context.request.user)
    user = context.request.user
    if user.is_authenticated:
        the_list = list_models.List.objects.get_or_none(user=user)
        if the_list is not None:
            return room in the_list.rooms.all()
        else:
            return False
    else:
        return False