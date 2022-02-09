from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
from django.urls import reverse


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


class Room(core_models.TimeStampedModel):

    """ Room Model Definiton """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
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
        (photo,) = self.photos.all()[
            :1
        ]  # 콤마 찍으면 실제로 원하는게 이array 의 첫번째 값이라는걸 알게됨 쿼리셋 아님
        return photo.file.url
