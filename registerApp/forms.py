# forms.py
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email']

    # def __init__(self, *args, **kwargs):
    #     super(UserProfileForm, self).__init__(*args, **kwargs)
    #     self.fields['profile_picture'].required = False
        
# class ReadlistForm(forms.Form):
#     title = forms.CharField(widget=forms.HiddenInput())
#     authors = forms.CharField(widget=forms.HiddenInput())
#     description = forms.CharField(widget=forms.HiddenInput())
#     thumbnail = forms.URLField(widget=forms.HiddenInput())

# class FavouritesForm(forms.Form):
#     title = forms.CharField(widget=forms.HiddenInput())
#     authors = forms.CharField(widget=forms.HiddenInput())
#     description = forms.CharField(widget=forms.HiddenInput())
#     thumbnail = forms.URLField(widget=forms.HiddenInput())
