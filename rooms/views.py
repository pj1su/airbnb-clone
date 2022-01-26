from django.http import Http404
from django.shortcuts import render, redirect, reverse

# from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

# from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from . import models


class HomeView(ListView):

    "HomeView Definition"

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     now = timezone.now()
    #     context["now"] = now
    #     return context
    # obj,page 들을 이 함수가 받아옴.


# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         # return redirect(reverse("core:home"))
#         raise Http404()
# 404.html은 자동적으로 404에러가 인식을 하는데 templates파일에 들어있어야 인식 다른 폴더안


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


class EditRoomView(UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name"
        "description"
        "country"
        "price"
        "city"
        "address"
        "guests"
        "beds"
        "bedrooms"
        "baths"
        "check_in"
        "check_out"
        "instant_book"
        "room_type"
        "amenity"
        "facility"
        "house_roul"
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room