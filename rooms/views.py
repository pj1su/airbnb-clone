from django_countries import countries
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy

# from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from users import mixins as user_mixins
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    View,
    FormView,
)
from . import models, forms

# ListView//// class view는 장고가 정해져있는걸 사용 function view는 사용자정의해서 내가 얻고싶은 값 얻어오기 가능
class HomeView(ListView):

    "HomeView Definition"

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"
    # template_name = "safehomes.html"
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


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "price",
        "city",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenity",
        "facility",
        "house_roul",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotoView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required  # 이 데코레이터는 setting에서 login url설정을 해야함
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        photo = models.Photo.objects.get(pk=photo_pk)
        if room.host.pk != user.pk or room.pk != photo.room.pk:
            messages.error(request, "Can't delete that photo")
            return redirect(reverse("core:home"))
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Delete")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Update"
    fields = ("caption",)

    def get_object(self, queryset=None):
        photo = super().get_object(queryset=queryset)
        if photo.room.host.pk != self.request.user.pk:
            raise Http404()
        return photo

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddphotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, FormView):

    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm
    # SuccessMessageMixin에는 from_valid , get_success_message가 있어서 messages를 써야함
    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Upload")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        # save m2m은 object가 database에 저장된 후에 사용해야함
        form.save_m2m()
        messages.success(self.request, "Create Room")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)
            # GET하면 빈 양식 인스턴스를 만들고 렌더링할 템플릿 컨텍스트에 배치합니다. 이것은 우리가 URL을 처음 방문할 때 일어날 것으로 예상할 수 있는 것입니다.

            # 요청 을 사용하여 양식이 제출 POST되면 보기는 다시 한 번 양식 인스턴스를 만들고 요청의 데이터로 채웁니다. 이것을 "양식에 데이터 바인딩"(이제 바인딩된 양식)이라고 합니다.form = NameForm(request.POST)

            # 우리는 양식의 is_valid()메소드를 호출합니다. 그렇지 않은 경우 True양식이 있는 템플릿으로 돌아갑니다. 이번에는 양식이 더 이상 비어 있지( 바인딩 해제 )되지 않으므로 HTML 양식은 이전에 제출된 데이터로 채워지며 필요에 따라 편집 및 수정할 수 있습니다.

            # is_valid()인 경우 이제 해당 속성 True에서 모든 검증된 양식 데이터를 찾을 수 있습니다 . cleaned_data이 데이터를 사용하여 데이터베이스를 업데이트하거나 HTTP 리디렉션을 브라우저에 보내기 전에 다음으로 이동할 위치를 알려주는 다른 처리를 수행할 수 있습니다.

            if form.is_valid():  # 폼에 에러가 하나도 없다면
                # print(form.cleaned_data)
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                host = form.cleaned_data.get("host")
                amenity = form.cleaned_data.get("amenity")
                facility = form.cleaned_data.get("facility")
                print(amenity)
                filter_args = {}
                # print(form.cleaned_data)
                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if host is True:
                    filter_args["host__superhost"] = True
                # print(filter_args)
                for amenities in amenity:
                    filter_args["amenity"] = amenities
                # print(amenities)
                # print(amenity, "start")
                for facilities in facility:
                    filter_args["facility"] = facilities
                    # rooms = rooms.filterQ["facility"]=facilities 이걸 Q쿼리로 해보기 그냥하면 오류 ex)filter(Q(<condition_1>) & Q(<condition_2>))

                qs = models.Room.objects.filter(**filter_args).order_by(
                    "-created"
                )  # paginator가 어떤 기준을 가지고 정렬할지 몰라서 필터로 무작위로 들고오니까

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        # if len(s_amenities) > 0:
        #     for s_amenity in s_amenities:
        #         rooms = rooms.filter(amenity__pk=int(s_amenity))

        # if len(s_facilities) > 0:
        #     for s_facility in s_facilities:
        #         rooms = rooms.filter(facility__pk=int(s_facility))
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
