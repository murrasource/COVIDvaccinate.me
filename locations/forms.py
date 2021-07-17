from django import forms
from .models import *

class SubscribeForm(forms.ModelForm):
    email = forms.EmailField(label="")
    zipcode = forms.IntegerField(label="")

    class Meta:
        model = Subscriber
        fields = ('email', 'state', 'zipcode')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Email', 'class': 'form-control'})
        self.fields['state'].widget.attrs.update({'class': 'form-control'})
        self.fields['zipcode'].widget.attrs.update({'placeholder': 'Zipcode', 'class': 'form-control'})

class UnsubscribeForm(forms.ModelForm):
    email = forms.EmailField(label="")

    class Meta:
        model = Subscriber
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Email', 'class': 'form-control'})
