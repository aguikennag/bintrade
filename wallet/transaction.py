from django.shortcuts import render
from django.views.generic import ListView,View,RedirectView,TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from urllib.parse import urlparse,urlunparse,urljoin
from .models import Wallet,WithdrawalApplication,Plan,PendingDeposit
from .forms import WithdrawalForm,AmountForm
from Users.models import Notification
from django.utils import timezone
import datetime



class EnterDepositAmount(LoginRequiredMixin,View)  :
    template_name = 'enter-amount.html'
    form_class = AmountForm
    model = Plan

    def get(self,request,*args,**kwargs) :
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
        _slug = kwargs.get('slug',None)
        if not _slug : return HttpResponse("Invalid request")
        try : plan = self.model.objects.get(slug =_slug)
        except self.model.DoesNotExist :
            return HttpResponse("Plan you selected does not exist")

        form = self.form_class(plan = plan,data = request.POST)
        if form.is_valid() :
            amount = form.cleaned_data['amount']
            return HttpResponseRedirect(reverse('deposit',args=[plan.slug,amount]))
        else :
            
            return render(request,self.template_name,locals())    

  

class Deposit(LoginRequiredMixin,View)  :
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
    template_name = 'withdrawal.html' 
    form_class  = WithdrawalForm

    def get(self,request,*args,**kwargs) :
        #verify you have no pending withdrawal
        if self.model.objects.filter(user = request.user).exists() :
            return HttpResponse("You already have a pending application,please wait for approval")
        #check if user has a plan
        if request.user.user_wallet.plan :
            #check if its ready for withdrawal
            if timezone.now() < request.user.user_wallet.plan_end : 
                return HttpResponse("You cant withdraw now as your investment has not reached maturity")
            amount = request.user.user_wallet.current_balance
            form = self.form_class(initial = {'amount' : amount})
        else : 
            return HttpResponse("You are not on any plan and can not widthdraw.Please subscribe to a plan to enable withdrawal" )   
            
        return render(request,self.template_name,locals())

    def post(self,request,*args,**kwargs) :
        #to do : on admin approval  deactivate user plan 
        form = self.form_class(request.POST) 
        if form.is_valid() :
            if self.model.objects.filter(user = self.request.user).exists() :
                return HttpResponse("You already have a pending application,please wait for approval")
            form.save(commit = False)
            form.instance.user = request.user
            form.save()
            msg = "Your withdrawal application has been submitted for processing,You will be notified once completed."
            Notification.objects.create(user = request.user,message = msg)
            url = urljoin(reverse('dashboard'),"?wthl=Cvxp") 
            return HttpResponseRedirect(url)
        else :
            return render(request,self.template_name,locals())    
     


class Invest(LoginRequiredMixin,TemplateView) :
    template_name = 'plans.html'

    def get_context_data(self,*args,**kwargs) : 
        context = super(Invest,self).get_context_data(*args,**kwargs) 
        context['plan'] = Plan.objects.filter(admin = self.request.user.admin.user_admin)
        return context
