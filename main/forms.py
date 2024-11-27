from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from main.models import ProductEntry, UserData

class CustomUserCreationForm(UserCreationForm):
    address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your address'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Save address in UserData
            UserData.objects.create(user=user, address=self.cleaned_data['address'])
        return user
        
    
class UserEditForm(UserChangeForm):
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your address'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email']

class ProductEntryForm(ModelForm):
    class Meta:
        model = ProductEntry
        fields = ["product_name", "product_desc", "price"]
