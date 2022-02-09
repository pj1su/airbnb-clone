from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    host = forms.BooleanField(required=False)
    amenity = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facility = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
