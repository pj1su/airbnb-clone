from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    accuracy = forms.IntegerField(max_value=5, min_value=1)
    communication = forms.IntegerField(max_value=5, min_value=1)
    cleanliness = forms.IntegerField(max_value=5, min_value=1)
    location = forms.IntegerField(max_value=5, min_value=1)
    check_in = forms.IntegerField(max_value=5, min_value=1)
    value = forms.IntegerField(max_value=5, min_value=1)
    #  어쩌면 모델에서 초이스로 하면 더 안전할 수 있다
    class Meta:
        model = models.Review
        fields = ("review",)

    def save(self):
        review = super().save(commit=False)
        return review
