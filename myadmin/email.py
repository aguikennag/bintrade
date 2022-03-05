from django.conf import settings
from django.views.generic import View,TemplateView,ListView,DetailView
from django.views.generic.edit import  DeleteView,UpdateView
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render

from core.mail import Email
from .forms import SendMailForm
from .dashboard import AdminBase
from wallet.models import Wallet


class SendCustomMail(AdminBase,View) :
    form_class = SendMailForm
    success_url = reverse_lazy('admin-dashboard')
    template_name = 'form.html'
    email_template = 'custom-email.html'


    def  get(self,request,*args,**kwargs)  :
        wallet_id = kwargs.get('wallet_id',None)
        if not wallet_id : 
            pass
        form = self.form_class()
        form_title = 'Send Custom Email'
        return render(request,self.template_name,locals())

           
           


    def  post(self,request,*args,**kwargs)  :
        try :
            self.receiver = Wallet.objects.get(wallet_id = self.kwargs['wallet_id']).user
        except KeyError :
            return HttpResponse("user id cannot be empty")  
        except Wallet.DoesNotExist :
            return HttpResponse("wallet id is not valid")   
        if not self.admin == self.receiver.admin :
            pass
        form = self.form_class(request.POST) 
        ctx = {}
        if form.is_valid() :
            sub = form.cleaned_data['subject']  
            message = form.cleaned_data['message']  
            mail = Email(send_type="support")
            ctx['message'] = message
            ctx['subject'] = sub
            ctx['site_name'] = settings.SITE_NAME
            ctx['client'] = self.receiver
            mail.send_html_email(["geeetech.inc@gmail.com"],sub,self.email_template,ctx)
            return HttpResponseRedirect(self.success_url)

        else : 
            return render(request,self.template_name,locals())




