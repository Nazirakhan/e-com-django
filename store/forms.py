from django import forms
from .models import ReviewRatings

# Create your models here.

class ReviewRatingsForm(forms.ModelForm):
    class Meta:
        model = ReviewRatings
        fields = ["subject","review","rating"]
