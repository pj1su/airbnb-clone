from django.db import models
from core import models as core_models

# from django.core import validators
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    # widget으로 리뷰점수 맥스,미니멈 조절가능한데 bulit validator 써서 조절
    review = models.TextField()
    accuracy = models.IntegerField(
        validators=[MinValueValidator(1), MinValueValidator(5)]
    )
    communication = models.IntegerField(
        validators=[MinValueValidator(1), MinValueValidator(5)]
    )
    cleanliness = models.IntegerField(
        validators=[MinValueValidator(1), MinValueValidator(5)]
    )
    location = models.IntegerField(
        validators=[MinValueValidator(1), MinValueValidator(5)]
    )
    check_in = models.IntegerField(
        validators=[MinValueValidator(1), MinValueValidator(5)]
    )
    value = models.IntegerField(validators=[MinValueValidator(1), MinValueValidator(5)])
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} -{self.room}"

    def rating_average(self):
        avg = (
            self.communication
            + self.accuracy
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "Avg."

    class Meta:
        ordering = ("-created",)
