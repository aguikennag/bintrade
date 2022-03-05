from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User,NewsLaterSubscriber



class UserCreateForm(UserCreationForm) :
    referral_id = forms.CharField(required  = False)

    class Meta(UserCreationForm.Meta) :
        model = User
        fields = UserCreationForm.Meta.fields + ('name','username','email','phone_number','country')

class ProfileUpdateForm(ModelForm) :
    class Meta() :
        model  = User
        fields = ['name','phone_number']

class SubscribeForm(forms.ModelForm)  :
    
    class Meta() :
        model = NewsLaterSubscriber
        fields = '__all__'

    def clean_email(self)   :
        email = self.cleaned_data['email'] 
        if self.Meta.model.objects.filter(email = email).exists() :
            raise forms.ValidationError("You have already subscribed !")
        return email