from dataclasses import fields
import email
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User,NewsLaterSubscriber,Settings


class SettingForm(ModelForm) :
    
    class Meta() :
        model = Settings
        exclude = ['user']

    def clean_email_on_transaction(self) :
        e_t = self.cleaned_data.get("email_on_transaction",False) 
        if e_t == "on" : e_t = True
        return e_t 

class VerifyEmailForm(forms.Form) :
    email = forms.EmailField(help_text="We are sending a verification code to this email address, you can edit it before hitting the send button")

    def __init__(self,user=None,*args,**kwargs) :
        self.user = user
        super(VerifyEmailForm,self).__init__(*args,**kwargs)
   

class WalletForm(ModelForm) :
 
    class Meta() :
        model  = User
        fields = ["_wallet_name","_wallet_address"]



class UserCreateForm(UserCreationForm) :
    referral_id = forms.CharField(required  = False)

    def __init__(self,*args,**kwargs) :
        super(UserCreateForm,self).__init__(*args,**kwargs)
        self.fields['email'].required = True

    class Meta(UserCreationForm.Meta) :
        model = User
        fields = UserCreationForm.Meta.fields + ('name','username','email','phone_number','country')


class ProfileForm(ModelForm) :

    def __init__(self,*args,**kwargs) :
        super(ProfileForm,self).__init__(*args,**kwargs)
        self.fields['email'].required = True

    class Meta() :
        model  = User
        fields = ['name','email','phone_number','country']
 

class SubscribeForm(forms.ModelForm)  :
    
    class Meta() :
        model = NewsLaterSubscriber
        fields = '__all__'

    def clean_email(self)   :
        email = self.cleaned_data['email'] 
        if self.Meta.model.objects.filter(email = email).exists() :
            raise forms.ValidationError("You have already subscribed !")
        return email