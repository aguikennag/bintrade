from django import forms
from django.core.exceptions import ValidationError
from .security import OTP

class OtpForm(forms.Form) :
    code = forms.CharField(required=True,help_text="Enter the code sent to your email,click resend if you dint get any after some time")
    

    def __init__(self,user=None,*args,**kwargs) :
        self.user = user
        super(OtpForm,self).__init__(*args,**kwargs)

     
    def clean_code(self) :
        code = self.cleaned_data['code']
        otp = OTP(self.user)
        validated,error = otp.validate_otp(code)
        if not validated :
            raise forms.ValidationError(error)
        return code     



