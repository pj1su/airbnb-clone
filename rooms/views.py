from django_countries import countries
from django.http import Http404
from django.shortcuts import render, redirect, reverse

# from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

# from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from . import models, forms

# ListView//// class view는 장고가 정해져있는걸 사용 function view는 사용자정의해서 내가 얻고싶은 값 얻어오기 가능
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


def search(request):
    country = request.GET.get("country")

    if country:
        form = forms.SearchForm(request.GET)

        if form.is_valid():  # 폼에 에러가 하나도 없다면
            # print(form.cleaned_data)
            city = form.cleaned_data("city")
            country = form.cleaned_data("country")
            room_type = form.cleaned_data("room_type")
            price = form.cleaned_data("price")
            guests = form.cleaned_data("guests")
            bedrooms = form.cleaned_data("bedrooms")
            beds = form.cleaned_data("beds")
            baths = form.cleaned_data("baths")
            instant_book = form.cleaned_data("instant_book")
            host = form.cleaned_data("host")
            amenity = form.cleaned_data("amenity")
            facility = form.cleaned_data("facility")
    else:
        form = forms.SearchForm()

    return render(request, "rooms/search.html", {"form": form})


# form 을 사용하면 GET.get받아온걸 int나boolean으로 안해도 데이터 정리를 해준다
# def search(request):
# city = request.GET.get("city", "Anywhere")
# city = str.capitalize(city)
# country = request.GET.get("country", "KR")
# room_type = int(request.GET.get("room_type", 0))
# price = int(request.GET.get("price", 0))
# guests = int(request.GET.get("guests", 0))
# bedrooms = int(request.GET.get("bedrooms", 0))
# beds = int(request.GET.get("beds", 0))
# baths = int(request.GET.get("baths", 0))
# instant = bool(request.GET.get("instant", False))
# superhost = bool(request.GET.get("superhost", False))
# s_amenities = request.GET.getlist("amenities")
# s_facilities = request.GET.getlist("facilities")

# # print(city)
# # request에서 받는건 폼으로 데이터베이스는 choices로 context에 비슷한 이름이 많아서 분리해주는것 그 후 merge
# form = {
#     "city": city,
#     "s_room_type": room_type,
#     "s_country": country,
#     "price": price,
#     "guests": guests,
#     "bedrooms": bedrooms,
#     "beds": beds,
#     "baths": baths,
#     "s_amenities": s_amenities,
#     "s_facilities": s_facilities,
#     "instant": instant,
#     "superhost": superhost,
# }

# room_types = models.RoomType.objects.all()
# amenities = models.Amenity.objects.all()
# facilities = models.Facility.objects.all()

# choices = {
#     "countries": countries,
#     "room_types": room_types,
#     "amenities": amenities,
#     "facilities": facilities,
# }

# filter_args = {}

# if city != "Anywhere":
#     filter_args["city__startswith"] = city

# filter_args["country"] = country

# if room_type != 0:
#     filter_args["room_type__pk"] = room_type

# if price != 0:
#     filter_args["price__lte"] = price

# if guests != 0:
#     filter_args["guests__gte"] = guests

# if bedrooms != 0:
#     filter_args["bedrooms__gte"] = bedrooms

# if beds != 0:
#     filter_args["beds__gte"] = beds

# if baths != 0:
#     filter_args["baths__gte"] = baths

# if instant is True:
#     filter_args["instant_book"] = True

# if superhost is True:
#     filter_args["host__superhost"] = True

# rooms = models.Room.objects.filter(**filter_args)

# if len(s_amenities) > 0:
#     for s_amenity in s_amenities:
#         rooms = rooms.filter(amenity__pk=int(s_amenity))

# if len(s_facilities) > 0:
#     for s_facility in s_facilities:
#         rooms = rooms.filter(facility__pk=int(s_facility))

# return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})


########## 13.6"search" nomadcoder commends
# rooms = models.Room.objects.filter(**filter_args)
# if len(s_amenities) > 0:
# s_amenities_query = Q(amenities__pk=int(s_amenities[0]))
# for s_amenity in s_amenities[1:]:
# s_amenities_query |= Q(amenities__pk=int(s_amenity))
# rooms = rooms.filter(s_amenities_query).distinct()

# if len(s_facilities) > 0:
# s_facilities_query = Q(facilities__pk=int(s_facilities[0]))
# for s_facility in s_facilities[1:]:
# s_facilities_query |= Q(facilities__pk=int(s_facility))
# rooms = rooms.filter(s_facilities_query).distinct() 이 방법은 or방법

# rooms = models.Room.objects.filter(**filter_args) 여기서부터 and 방법 Q쿼리로

# if len(s_amenities) >0:
# amenity_query = Q(amenities = s_amenities[0])
# for s_amenity in s_amenities[1:]:
# amenity_query &= Q(amenities = s_amenity)
# rooms = rooms.filter(amenity_query)

# if len(s_facilities) > 0:
# facility_query = Q(facility = s_facilities[0])
# for s_facility in s_facilities[1:]:
# facility_query &= Q(facility = s_facility)
# rooms = rooms.filter(facility_query)