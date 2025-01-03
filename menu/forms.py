from django import forms
from .models import Category , FoodItem
from accounts.validators import allow_only_images_validator

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['category_name','description']

    
class FoodItemForm(forms.ModelForm):
    image = forms.FileField(validators=[allow_only_images_validator])
    class Meta:
        model=FoodItem
        fields=['food_title','description','price','category','image','is_available']