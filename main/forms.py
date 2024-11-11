from django.forms import ModelForm
from main.models import ProductEntry #MoodEntry,

# class MoodEntryForm(ModelForm):
#     class Meta:
#         model = MoodEntry
#         fields = ["mood", "feelings", "mood_intensity"]


class ProductEntryForm(ModelForm):
    class Meta:
        model = ProductEntry
        fields = ["product_name", "product_desc", "price"]
