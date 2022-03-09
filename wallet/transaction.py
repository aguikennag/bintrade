from django.shortcuts import render
from django.views.generic import ListView,View,RedirectView,TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from urllib.parse import urlparse,urlunparse,urljoin
from .models import Wallet,WithdrawalApplication,Plan,PendingDeposit
from .forms import WithdrawalForm,DepositForm
from Users.models import Notification
from myadmin.models import Settings as AdminSetting
from django.utils import timezone
from django.contrib import messages
import datetime



class Deposit(LoginRequiredMixin,View)  :
    template_name = 'deposit.html'
    form_class = DepositForm
    model = Plan

    def get(self,request,*args,**kwargs) :
         #check if user has pending deposit
        if PendingDeposit.objects.filter(user = request.user,is_approved = False).exists() :
            return HttpResponse("You have a pending deposit already do wait for approval,thank You")    
        if not request.user.user_wallet.allowed_to_invest :
            return HttpResponse("Your plan is still active,you cannot make another innvestment at this time")
        _slug = kwargs.get('slug',None)
        if not _slug : return HttpResponse("Invalid request")
        try : plan = self.model.objects.get(slug =_slug)
        except self.model.DoesNotExist :
            return HttpResponse("Plan you selected does not exist")
        form = self.form_class    
        return render(request,self.template_name,locals())

    def post(self,request,*args,**kwargs) : 
         #check if user has pending deposit
        if PendingDeposit.objects.filter(user = request.user,is_approved = False).exists() :
            return HttpResponse("You have a pending deposit already do wait for approval,thank You")    
        if not request.user.user_wallet.allowed_to_invest :
            return HttpResponse("Your plan is still active,you cannot make another innvestment at this time")

        try : plan = self.model.objects.get(pk = self.request.POST['plan'])
        except self.model.DoesNotExist :
            return HttpResponse("Plan you selected does not exist")
        except KeyError :
            return HttpResponse("invalid request")

        form = self.form_class(plan,request.POST,request.FILES)

        if form.is_valid() :
            form.save(commit=False)
            form.instance.plan = plan
            form.instance.user = request.user
            form.save()
            messages.success(request,"Your deposit transaction has been registered and is being processed, you will be notified when processing is completed.") 
            return HttpResponseRedirect(reverse('dashboard'))
        else :
            
            print(form.errors)
            return render(request,self.template_name,locals())    

  

class Deposigt(LoginRequiredMixin,View)  :
    model = Wallet
    model_p = Plan
    template_name = 'deposit.html'

    def get(self,request,*args,**kwargs) :
        
        _slug = kwargs.get('slug',None)
        amount  = kwargs.get('amount',None)
        if not _slug or not amount : return HttpResponse("Invalid request")
        try : 
            plan = self.model_p.objects.get(slug =_slug)
            if not amount <= plan.max_cost and not amount >= plan.min_cost :
                return "Entered amount is not valid for the selected plan"
        except self.model_p.DoesNotExist :
            return HttpResponse("Plan you selected does not exist")
        return render(request,self.template_name,locals())

    def post(self,request,*args,**kwargs) :    
        return HttpResponse("Invalid")




class DepositComplete(LoginRequiredMixin,View)  :
    model = Wallet
    model_p = Plan
    template_name = 'deposit.html'

    def get(self,request,*args,**kwargs) :
        _slug = kwargs.get('slug',None)
        coin = kwargs.get('coin',None)
        amount  = kwargs.get('amount',None)
        if not _slug or not coin or not amount : return HttpResponse("Invalid request")
        try : plan = self.model_p.objects.get(slug =_slug)
        except self.model_p.DoesNotExist :
            return HttpResponse("Plan you selected does not exist")
        
        #check if user has pending deposit
        if not PendingDeposit.objects.filter(user = request.user,is_approved = False).exists() :
            msg = "You deposit has been acknowledged and is now processing,you will be notified shortly" 
            Notification.objects.create(user = request.user,message = msg)
            #create pending deposit 
            PendingDeposit.objects.create(user = request.user,plan = plan,coin = coin,amount = amount) 
            url = urljoin(reverse('dashboard'),"?dpt=hsdvv") 
            return HttpResponseRedirect(url)
        else :
            return HttpResponse("You have a pending deposit already do wait for approval,thank You")    

    def post(self,request,*args,**kwargs) :    
        return HttpResponse("Invalid")




class Withdrawal(LoginRequiredMixin,View)  :  
    model = WithdrawalApplication
    template_name = 'withdraw.html' 
    form_class  = WithdrawalForm

    def withdrawal_allowed(self) :
        try :
            withdrawal_allowed = AdminSetting.objects.all()[0].enable_withdrawal
        except : withdrawal_allowed = False
        return withdrawal_allowed

    def get(self,request,*args,**kwargs) :  
        withdrawal_allowed = self.withdrawal_allowed()
        return render(request,self.template_name,locals())


    def post(self,request,*args,**kwargs) :
        #to do : on admin approval  deactivate user plan 
        withdrawal_allowed = self.withdrawal_allowed()
        if not  withdrawal_allowed :
            return HttpResponse("Fund withdrawals are not available at the moment, we are working to bring it back ASAP. please check back in a moment")
        
        if not request.user.wallet_address_valid :
            return HttpResponse("""You are yet to enter a valid wallet address, you can't proceed with a withdrawal. Please <a href="{% url 'profile' %}?tab=wallet-address">provide a valid wallet address for payment""")
        
        form = self.form_class(user = request.user,data = request.POST) 
        if form.is_valid() :     
            form.save(commit = False)
            form.instance.user = request.user
            form.save()
            msg = "Your withdrawal application has been submitted for processing,You will be notified once completed."
            messages.success(request,msg)
            Notification.objects.create(user = request.user,message = msg)
           
            return HttpResponseRedirect(reverse('dashboard'))
        else :
            return render(request,self.template_name,locals())    
     


class Invest(LoginRequiredMixin,ListView) :
    template_name = 'plans.html'
    model = Plan
    context_object_name = "plans"