from django.views.generic import CreateView,View,TemplateView,ListView,DetailView
from django.views.generic.edit import  DeleteView,UpdateView
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.shortcuts import render 
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.utils import timezone

from core.mail import Email
from wallet.models import Plan,Transaction,PendingDeposit,WithdrawalApplication
from Users.models import Notification
from .dashboard import AdminBase



class CreatePlan(AdminBase,CreateView) :
    model = Plan
    success_url = reverse_lazy('plans-admin')
    template_name = 'form.html'
    fields = ['name','min_cost','max_cost','interest_rate','duration']

    def form_valid(self,form) :
        form.save(commit = False)
        form.instance.admin = self.request.user.user_admin
        form.save()
        return HttpResponseRedirect(self.success_url)


 
class AllPlans(AdminBase,ListView) :
    model  = Plan
    template_name = 'plan-list.html'    
    context_object_name = "plans"

    def get_queryset(self) :
        return self.model.objects.filter(admin = self.request.user.user_admin)    



class DepositNotice(AdminBase,ListView)   :
    model = PendingDeposit    
    template_name = 'deposit-notice.html'    
    context_object_name = "deposits" 

    def get_queryset(self) :
        return self.model.objects.filter(user__admin = self.request.user,is_approved = False)    


class ApproveDeposit(View) :
    model = PendingDeposit

    def on_approved_deposit(self,instance) :
        #fund user wallet
        wallet = instance.user.user_wallet
        wallet.plan = instance.plan
        wallet.plan_start = timezone.now()
        wallet.plan_end = timezone.now() + timezone.timedelta(days = int(instance.plan.duration))
        wallet.initial_balance = instance.amount
        wallet.expected_maximum_balance = instance.amount +  instance.plan.get_interest(instance.amount)
        wallet.plan_is_active = True
        
        #notify user 
        msg = "Your ${} deposit has been approved.".format(instance.amount)
        Notification.objects.create(user = instance.user,message = msg)
        
        #create transaction
        Transaction.objects.create(user = instance.user,
        status = "Approved",
        amount = instance.amount,
        transaction_type = 'DEPOSIT',
        coin = instance.coin,
        description = "Deposit Approved"
        )    
        wallet.save()
        return
        

    def send_email(self,dp)   :
        mail = Email("alert")
        mail.deposit_email(dp)
        


    def get(self,request,*args,**kwargs) :
        feedback = {}
        pk = request.GET.get('pk',None)
        if not pk :
            feedback['error'] = "Incomplete request Parameters"
            return JsonResponse(feedback)
        try : 
            pd = self.model.objects.get(pk = pk)
            
            if not pd.user.admin == request.user :
                feedback['error'] = "You are not authorized to perform this action"
                return JsonResponse(feedback)
            else : 
                self.on_approved_deposit(pd)  
                if request.user.user_admin.settings.enable_transaction_emails :
                    #self.send_email(pd)  
                    pass
                #delete pending
                pd.delete()
                feedback['success'] = True
                return JsonResponse(feedback)
        except self.model.DoesNotExist :
            feedback['error'] = "this deposit does no longer exist"
            return JsonResponse(feedback)
        return JsonResponse(feedback)


class DeclineDeposit(AdminBase,View)   :
    pass



class WithdrawalRequest(AdminBase,ListView) :
    model = WithdrawalApplication
    template_name = 'withdrawal_application.html'
    context_object_name = 'withdrawals'

    
    def get_queryset(self) :
        return self.model.objects.filter(user__admin = self.request.user).order_by('-date')

