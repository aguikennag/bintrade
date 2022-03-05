from django.shortcuts import render
from django.views.generic import RedirectView,View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string,get_template
from django.conf import settings
from django.utils import timezone


from io import BytesIO

import random



class ValidationCode()     :
    @staticmethod
    def generate_code(user,email=None,phone_number=None,offset = None,send_type = 'message') :
        """ offset is the active time for the code,
        """
        offset = offset or 5
        expiry = timezone.now() + timezone.timedelta(minutes=offset)
        code = random.randrange(99999,999999)
        db = user.dashboard
        db.otc = int(code)
        db.otc_expiry = expiry
        db.save()
        ctx = {'expiry' : expiry.time(),'code' : code}
        email_receiver = user.email
        #payload = self.convert_html_to_pdf(template_name,ctx)
        name = user.name or user.username
             
        
        if send_type == 'message' :
            msg = "credo capital bank phone number verification code is {}".format(code)
            sms = Messages()
            sms.send_sms(phone_number,msg)


        elif send_type == 'email' :
            subject = "Credo Capital email verification"
            mail = Email(send_type='support')
            ctx['name'] = name
            mail.send_html_email([email_receiver],subject,"otp-email.html",ctx=ctx)


    @staticmethod
    def validate_otc(user,code) :
        """
        returns a tuple of the validations state and error  if theres any or None as 2nd index
        """
        if user.dashboard.otc == int(code) :
            if not timezone.now() < user.dashboard.otc_expiry :
                error = "The entered code is correct,but has expired"
                return (False,error)
            else : 
                return (True,None)  

        else :
            return (False,"The entered code is incorrect")  

        return (False,"unknown error occured")           




class Email() :

    def __init__(self,send_type = "support") :
        from django.core.mail import get_connection
        host = settings.EMAIL_HOST
        port = settings.EMAIL_PORT
        if send_type == "support" :
            password = "Kyletech99"
        else :
            password = "Kyletech99"    
        senders = {'alert' : settings.EMAIL_HOST_USER_ALERT,
        'support' : settings.EMAIL_HOST_USER_SUPPORT }
        self.send_from = senders.get(send_type,senders['alert'])
        self.auth_connecion = get_connection(
            host = host,
            port = port,
            username = self.send_from,
            password = password,
            use_tls = settings.EMAIL_USE_TLS
        ) 



    def send_email(self,receive_email_list,subject,message,headers=None) :
        headers = {
            'Content-Type' : 'text/plain'
        } 
        try : 
            email = EmailMessage(subject = subject,body=message,
            from_email=self.send_from,to=receive_email_list,
            headers = headers,connection=self.auth_connecion)
            email.send()
            self.auth_connecion.close()
        except :
            pass


    def send_html_email(self,receive_email_list,subject,template,ctx=None) :
        msg = render_to_string(template,ctx)
        email = EmailMessage(subject,msg,self.send_from,receive_email_list,connection=self.auth_connecion)
        email.content_subtype = "html"
        email.send()
        self.auth_connecion.close()
        


    def send_file_email(self,file_name,_file,receive_email_list,subject,message) :
        email = EmailMessage(subject,message,self.send_from,receive_email_list,connection=self.auth_connecion)
        email.attach(file_name,_file)
        try : 
            email.send()
            self.auth_connecion.close()
        except : pass

    

    def deposit_email(self,deposit_obj) :
        pd = deposit_obj
        ctx = {   
        }   
        subject = settings.SITE_NAME + " Transaction alert"
        email_receiver = pd.user.email
        name = pd.user.username
        ctx['site_full_address'] = settings.SITE_ADDRESS
        ctx['name'] = name
        ctx['deposit_id'] = "{}".format(pd.pk)
        ctx['wallet_name'] = pd.user.name
        ctx['wallet_id'] = pd.user.user_wallet.wallet_id
        ctx['amount'] = pd.user.user_wallet.initial_balance
      
        ctx['coin'] = name
        ctx['balance'] = pd.user.user_wallet.current_balance
        ctx['date'] = pd.date
        ctx['site_name'] = settings.SITE_NAME
        self.send_html_email([email_receiver],subject,"transaction-email.html",ctx=ctx)
        
    
    def transaction_email(self,transact_obj) :
        ctx = {}
        sub = "Transaction Email Alert"
        ctx['site_name'] = settings.SITE_NAME
        ctx['subject'] = "{} Transaction Alert".format(settings.SITE_NAME)
        ctx['client'] = transact_obj.user
        ctx['transact'] = transact_obj
        ctx['site_email'] = settings.EMAIL_HOST_USER 
       
        self.send_html_email(["geeetech.inc@gmail.com"],sub,"transaction-email.html",ctx)


    def welcome_email(self,client) :
        subject = "welcome To {}".format(settings.SITE_NAME)
        ctx =  {'client' : client,'site_name' : settings.SITE_NAME}
        self.send_html_email([client.email],subject,"welcome-email.html",ctx = ctx)
        
   