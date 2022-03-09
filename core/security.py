
from django.conf import settings
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.core.validators import validate_email

import random
from .mail import Email
from Users.models import Security



class OTP() :
    model = Security

    def __init__(self,user) :
        self.user = user 

    
    def generate_and_send_code(self,email=None,phone_number=None,offset = None,target = 'sms') :
        """ offset is the active time for the code in minutes,
        """
        user = self.user
        offset = offset or 5
        expiry = timezone.now() + timezone.timedelta(minutes=offset)
        code = random.randrange(99999,999999)
        sk,_ = self.model.objects.get_or_create(user = user)
        sk.otp = int(code)
        sk.otp_expiry = expiry
        sk.save()
        ctx = {'expiry' : expiry.time(),'code' : code}
        email_receiver = email or user.email
        #payload = self.convert_html_to_pdf(template_name,ctx)
        name = user.name or user.username
        msg = "Hello {},use {} as your {} verification code. please never share this code with anyone .".format(
                user.name,
                code,
                settings.SITE_NAME,
                )


        if target == 'mail' :
            if not email :
                return  "email cannot be none for target as mail"
            try : validate_email(email)
            except ValidationError : 
                return """The entered email address failed vaildation, 
                please enter a valid email address"""    
            
            subject = "{} email verification".format(settings.SITE_NAME)
            mail = Email(send_type='support')
            ctx['name'] = name
            mail.send_email([email_receiver],subject,msg)
        
        else :
            return "Something went wrong, it must be from our part please contact support"


    def validate_otp(self,code) :
        """
        returns a tuple of the validations state and error  if theres any or None as 2nd index
        """
        try : code = int(code)
        except :
            return (False,"The entered code is invalid")
        try :
            sk = self.model.objects.get(user = self.user)
        except self.model.DoesNotExist  :
            return(False,"An error occured while validating, seems no otp has been sent to you, resend otp .")    
        
        if sk.otp == code :
            if not timezone.now() < sk.otp_expiry :
                error = "The entered code is correct, but has expired"
                return (False,error)
            else : 

                return (True,None)  

        else :
            return (False,"The entered code is incorrect")  

              

class SendOtp(LoginRequiredMixin,View) :
    def get(self,request,*args,**kwargs) :
        feedback = {}
        target = kwargs.get("target",None)
        if not target :
            feedback['error'] = "Incomplete request"
            return JsonResponse(feedback)

        if target == "mail"  :
            email = request.GET.get('email',None)
            if not email :
                feedback['error'] = "Email cannot be empty"
                return JsonResponse(feedback)
            kwargs = {"target" : "mail", "email" : email}

        elif target == "sms" :
            phone_number = request.GET.get("phone_number",None)
            if not phone_number :
                feedback['error'] = "Phone number cannot be empty"
                return JsonResponse(feedback)
            kwargs = {"target" : "sms", "phone_number" : phone_number}

        otp = OTP(request.user)    
        error = otp.generate_and_send_code(**kwargs)
       
        if error : 
            #status should normally be None
            feedback['error'] = error
            return JsonResponse(feedback)
        feedback['success'] = 'Your verification code has been sent successfully,please check your {}'.format(target)
        
        
        return JsonResponse(feedback)