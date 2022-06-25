from dataclasses import fields
import email
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User,NewsLaterSubscriber,Settings,KYC


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

    def clean_password1(self) :
        password1 = self.cleaned_data.get("password1")

        if not password1 : 
            raise forms.ValidationError("password cannot be empty") 

        if len(password1) < 4 : 
            raise forms.ValidationError("password is too short, must be atleast 4 characters")
        
        return password1

    def clean_password2(self) :
        
        password1  = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password1 or not password2 : 
            raise forms.ValidationError("password cannot be empty") 

        if password1 !=  password2  : 
            raise forms.ValidationError("password must match ")
        
        return password2    

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


class KycForm(forms.ModelForm) :


    class Meta() :
        model = KYC
        exclude = ['user','is_accepted','date']
