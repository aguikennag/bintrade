from __future__ import absolute_import
import email
from email.mime.image import MIMEImage
from django.shortcuts import render
from django.views.generic import RedirectView,View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string,get_template
from django.conf import settings
from django.utils import timezone



import os.path
import re
import uuid
#from email.MIMEBase import MIMEBase

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, SafeMIMEMultipart



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
             
  

        if send_type == 'email' :
            subject = "Zealkoin ltd. email verification"
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


class EmailMultiRelated(EmailMultiAlternatives):
    """
    A version of EmailMessage that makes it easy to send multipart/related
    messages. For example, including text and HTML versions with inline images.
    
    @see https://djangosnippets.org/snippets/2215/
    """
    related_subtype = 'related'
    
    def __init__(self, *args, **kwargs):
        # self.related_ids = []
        self.related_attachments = []
        return super(EmailMultiRelated, self).__init__(*args, **kwargs)
    

    def attach_related(self, filename=None, content=None, mimetype=None):
        """
        Attaches a file with the given filename and content. The filename can
        be omitted and the mimetype is guessed, if not provided.

        If the first parameter is a MIMEBase subclass it is inserted directly
        into the resulting message attachments.
        """
        if isinstance(filename, MIMEBase):
            assert content == mimetype == None
            self.related_attachments.append(filename)
        else:
            assert content is not None
            self.related_attachments.append((filename, content, mimetype))
    
    def attach_related_file(self, path, mimetype=None):
        """Attaches a file from the filesystem."""
        filename = os.path.basename(path)
        content = open(path, 'rb').read()
        self.attach_related(filename, content, mimetype)
    
    def _create_message(self, msg):
        return self._create_attachments(self._create_related_attachments(self._create_alternatives(msg)))
    
    def _create_alternatives(self, msg):       
        for i, (content, mimetype) in enumerate(self.alternatives):
            if mimetype == 'text/html':
                for related_attachment in self.related_attachments:
                    if isinstance(related_attachment, MIMEBase):
                        content_id = related_attachment.get('Content-ID')
                        content = re.sub(r'(?<!cid:)%s' % re.escape(content_id), 'cid:%s' % content_id, content)
                    else:
                        filename, _, _ = related_attachment
                        content = re.sub(r'(?<!cid:)%s' % re.escape(filename), 'cid:%s' % filename, content)
                self.alternatives[i] = (content, mimetype)
        
        return super(EmailMultiRelated, self)._create_alternatives(msg)
    
    def _create_related_attachments(self, msg):
        encoding = self.encoding or settings.DEFAULT_CHARSET
        if self.related_attachments:
            body_msg = msg
            msg = SafeMIMEMultipart(_subtype=self.related_subtype, encoding=encoding)
            if self.body:
                msg.attach(body_msg)
            for related_attachment in self.related_attachments:
                if isinstance(related_attachment, MIMEBase):
                    msg.attach(related_attachment)
                else:
                    msg.attach(self._create_related_attachment(*related_attachment))
        return msg
    
    def _create_related_attachment(self, filename, content, mimetype=None):
        """
        Convert the filename, content, mimetype triple into a MIME attachment
        object. Adjust headers to use Content-ID where applicable.
        Taken from http://code.djangoproject.com/ticket/4771
        """
        attachment = super(EmailMultiRelated, self)._create_attachment(filename, content, mimetype)
        if filename:
            mimetype = attachment['Content-Type']
            del(attachment['Content-Type'])
            del(attachment['Content-Disposition'])
            attachment.add_header('Content-Disposition', 'inline', filename=filename)
            attachment.add_header('Content-Type', mimetype, name=filename)
            attachment.add_header('Content-ID', '<%s>' % filename)
        return attachment



class Email() :

    def __init__(self,send_type = "support") :
        from django.core.mail import get_connection
        host = settings.EMAIL_HOST
        port = settings.EMAIL_PORT
        password =    settings.EMAIL_HOST_PASSWORD  
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
        
        self.default_subject = "{} {}".format(
            settings.SITE_NAME,
            send_type
        )
        self.default_template = "custom-mail.html"


    def send_email(self,receive_email_list,subject,message,headers=None) :
        headers = {
            'Content-Type' : 'text/plain'
        } 
        
        email = EmailMessage(subject = subject,body=message,
        from_email=self.send_from,to=receive_email_list,
        headers = headers,connection=self.auth_connecion)
        try :
            email.send()
        except : pass    
        self.auth_connecion.close()
      

    def send_html_email(self,receive_email_list,template = None,subject =None,files_path_list=None,ctx=None) :
        subject = subject or self.default_subject
        template = template or self.default_template
        ctx = ctx
        ctx['site_name'] = settings.SITE_NAME
        msg = render_to_string(template,ctx)
        
        email = EmailMultiAlternatives(
            subject,
            msg,
            self.send_from,
            receive_email_list,
            connection=self.auth_connecion
            )
        email.content_subtype = "html"
        email.mixed_subtype = "related"
        #email.mixed_subtype = 'related'
        BASE_DIR = settings.STATIC_URL
        logo_path = os.path.join(settings.BASE_DIR,"static/main-theme/img/logo.png")
        with open(logo_path,'rb') as f :
            logo = MIMEImage(f.read())
            logo.add_header("Content-ID","<logo.png>")
            email.attach(logo)
            
        """if isinstance(files_path_list,list) :
            for file in files_path_list :
                "fetch image"
                with open(file,"rb") as f :
                    image = MIMEImage(f.read())"""
        """with open(logo_path, mode='rb') as f :
            image = MIMEImage(f.read())
            email.attach(image)
            image.add_header('Content-ID',"<logo>") """        
        
        email.send()
        
    
        


    def send_file_email(self,file_name,_file,receive_email_list,subject,message) :
        email = EmailMessage(subject,message,self.send_from,receive_email_list,connection=self.auth_connecion)
        email.attach(file_name,_file)
        try : 
            email.send()
            self.auth_connecion.close()
        except : pass

    def send_withdrawal_mail(self,withdrawal_object) :
        ctx = {
            'name' : withdrawal_object.user.name,
            'text' : """
            <p>This is to inform you that {0} worth of ${1} has been sent to your wallet successfully
            </p>
            <p>Find below the details  the transaction:</p>
            <strong>Amount : ${1}</strong><br>
            <strong>Payment Mode : {0}</strong><br>
            <strong>User : {2}</strong><br>
            <strong>Bitcoin Address :{3} </strong><br>
            <strong>Transaction Batch : {4}</strong><br>
            <p>Thanks For Choosing Zealkoin.ltd</p>
            <p></p><br>
            <a href="zealkoin.ltd">zealkoin.ltd</a><br>
            <span>©️ 2022 zealkoin.ltd Investment Platform .</span><br>
            <em>All Rights Reserved</em>
            """.format(
            withdrawal_object.user._wallet_name,
            withdrawal_object.amount,
            withdrawal_object.user.username,
            withdrawal_object.user._wallet_address,
            str(uuid.uuid1()).replace("-","") +  str(uuid.uuid1()).replace("-","")
        
            )
        }
        
        self.send_html_email(
            [withdrawal_object.user.email],
            subject = "Debit Transaction alert",
            ctx = ctx
        )
    

    def send_deposit_mail(self,deposit_object) :
        ctx = {
                'name' : deposit_object.user.name,
                'text' : """
                <p>This is to inform you that your deposit of ${0} has been approved, and your {1} wallet has been credited.
                </p>
                <p>Find below the details  the transaction:</p>
                <strong>Amount : ${0}</strong><br>
                <strong>Payment Mode : {2}</strong><br>
                <strong>User : {3}</strong><br>
    
                <strong>Transaction Batch : {4}</strong><br>
                <p>Thanks For Choosing Zealkoin.ltd</p>
                <p></p><br>
                <a href="zealkoin.ltd">zealkoin.ltd</a><br>
                <span>©️ 2022 zealkoin.ltd Investment Platform .</span><br>
                <em>All Rights Reserved</em>
                """.format(
                deposit_object.amount,
                settings.SITE_NAME,
                deposit_object.payment_method,
                deposit_object.user.username,
                str(uuid.uuid1()).replace("-","") +  str(uuid.uuid1()).replace("-","")
                #"usdguyfusfsdhsdusdusudyuysd"

             )
        }

        self.send_html_email(
            [deposit_object.user.email],
            subject = "Credit Transaction alert",
            ctx = ctx
        )


    def send_investment_mail(self,investment_object) :

        ctx = {}
        ctx['name'] = investment_object.user.name
        ctx['text'] =  """
        <p>This is to inform you that your ${0} investment for the 
        {1} {2} plan has been processed, and initiated.
        </p>
        <p>Find below the details  the transaction :</p>
        <strong>Amount : ${0}</strong><br>
        <strong>User : {3}</strong><br>
        <strong>Start Date : {4}</strong><br>
        <strong>Date Due : {5} </strong><br>
        <strong>Expected Interest : {6}</strong><br>
        <p>Thanks For Choosing Zealkoin.ltd</p>
        <p></p><br>
        <a href="zealkoin.ltd">zealkoin.ltd</a><br>
        <span>©️ 2022 zealkoin.ltd Investment Platform .</span><br>
        <em>All Rights Reserved</em>
        """.format(
        investment_object.amount,
        settings.SITE_NAME,
        investment_object.plan.name,
        investment_object.user.username,
        investment_object.plan_start.date,
        investment_object.plan_end.date,
        investment_object.expected_earning


        )
        subject = "Investment processed"
        self.send_html_email([investment_object.user.email],subject = subject,ctx = ctx)
   
   
    def welcome_email(self,client) :
        subject = "welcome To {}".format(settings.SITE_NAME)
        ctx =  {'client' : client,'site_name' : settings.SITE_NAME}
        self.send_html_email([client.email],subject,"welcome-email.html",ctx = ctx)
        
   