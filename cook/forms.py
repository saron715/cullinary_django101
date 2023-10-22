from django import forms 
from django.forms import ModelForm
from .models import Review,Recipe

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['rating', 'comment']

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'image', 'cuisine_type']        