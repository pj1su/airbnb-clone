from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
from django.urls import reverse
from cal import Calender
from django.utils import timezone


class AbstractItem(core_models.TimeStampedModel):
    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Object Definition """

    class Meta:
        verbose_name = "Room Type"
        ordering = ["created"]


class Amenity(AbstractItem):

    """ Amenity Object Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Modle Definition """

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


# 원래 Room보다 위에 있으면 에러가 나오는데 "Room"처럼 스트링만 있으면 장고는 어떤 모델을 말하는지 알 수 있다


class Room(core_models.TimeStampedModel):

    """ Room Model Definiton """

    name = models.CharField(max_length=140)
    description = models.TextField(max_length=140)
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()  # DemicalField는 소수점도 나옴
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="How many people will be staying?")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenity = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facility = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_roul = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *arg, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*arg, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def tatal_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 1)
        else:
            return 0

    def first_photo(self):
        # print(self.photos.all()[:1])
        # one ,two, three, four =self.photos.all()[:1] 하면 첫번째 array는 one이런식으로 들어가서 내가 원하는 쿼리셋을 얻어올 수 있다
        try:
            (photo,) = self.photos.all()[:1]
            # 콤마 찍으면 실제로 원하는게 이array 의 첫번째 값이라는걸 알게됨 쿼리셋 아님
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    # def get_beds(self):
    #     if self.beds == 1:
    #         return "1 bed"
    #     else:
    #         return f"{self.beds} beds"

    def get_calender(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = this_month + 1
        this_month_cal = Calender(this_year, this_month)
        if this_month == 12:
            next_month = 1
            this_year += 1
        next_month_cal = Calender(this_year, next_month)
        return [this_month_cal, next_month_cal]

        # if this_month != 12:
        #     this_year
        # else:
        #     this_year + 1
        # if this_month != 12:
        #     this_month + 1
        # else:
        #     1
