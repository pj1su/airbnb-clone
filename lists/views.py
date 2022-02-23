from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from rooms import models as room_models
from . import models


def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        the_list, _ = models.List.objects.get_or_create(
            user=request.user, name="My Favourites House"
        )
        # get이라서 하나밖에 못찾음 2개이상찾으면 error반환
        if action == "add":
            the_list.rooms.add(
                room
            )  # manytomany는 save말고 add 등 set,clear,create,filter 등 많이 할 수 있다
        elif action == "remove":
            the_list.rooms.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(TemplateView):

    template_name = "lists/list_detail.html"