from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from Users.models import Notification
from myadmin.models import MyAdmin
import random
import math
import uuid


class Plan(models.Model) :
    admin = models.ForeignKey(MyAdmin,on_delete = models.CASCADE,related_name = 'plans')
    name = models.CharField(max_length=40,help_text = "name you wish to call the investment plan")
    slug = models.SlugField(blank = True)
    max_cost = models.FloatField(null = True,blank = True,help_text = "maximum investment for thie plan,currency is USD")   #in $usd
    min_cost = models.FloatField(help_text = "minimum investment for thie plan,currency is USD")   #in $usd
    duration = models.PositiveIntegerField(help_text = "plan duration in days")  #in days
    interest_rate = models.FloatField(blank = False,null = False,help_text = "in %,e.g 50,100,200")
    date = models.DateField(auto_now_add= True)

    def __str__(self) :
        return self.name

    def get_interest(self,amount) :
        return (self.interest_rate/100) * amount  

    @property
    def active_subscribers(self) :
        return self.wallet_subscribers.filter(plan_is_active = True).count()         


    def save(self,*args,**kwargs) :
        self.slug = slugify(self.name)
        super(Plan,self).save(*args,**kwargs)


    class Meta() :
        ordering = ['min_cost']         



class Currency(models.Model) :
    admin = models.ForeignKey(MyAdmin,on_delete = models.CASCADE,related_name = 'currency')
    name = models.CharField(max_length=10)
    code = models.CharField(max_length=10)

    def __str__(self) :
        return self.name



class Wallet(models.Model) :
    CURRENCY = (('USD','USD'),('BPD','BPD'))
    wallet_id = models.UUIDField(default = uuid.uuid4,editable = False,null = False)
    user = models.OneToOneField(get_user_model(),related_name = 'user_wallet',on_delete = models.CASCADE)
    #preferred_currency = models.ForeignKey(Currency,on_delete=models.CASCADE,related_name = 'currency')
    plan = models.ForeignKey(Plan,related_name = 'wallet_subscribers',null = True,blank = True,on_delete = models.SET_NULL)
    plan_start = models.DateTimeField(null = True,blank = True)
    plan_end = models.DateTimeField(null = True,blank = True)
    #becomes value of plan when user invests
    initial_balance = models.FloatField(default=0.0,blank = True,)  #equal to entered amount
    #bonus_amount = models.FloatField(blank = True,null = True)  #fadmin can set amount to override current balance calculation
    expected_maximum_balance = models.FloatField(default = 0.0,blank = True) #at the end of the plan
    referral_earning = models.FloatField(default = 0.0)
    past_deposit_earning = models.FloatField(default = 0.0)
    funded_earning = models.FloatField(default = 0.0) 
    withdrawals = models.FloatField(default = 0.0) 
    plan_is_active = models.BooleanField(default = False,blank = True)
    previous_plan = models.ForeignKey(Plan,related_name = 'previous_plan',null = True,blank = True,on_delete = models.SET_NULL)
    
    @property
    def plan_is_due(self) :
        if timezone.now()   ==   self.plan_end :
            return True
        return False 



    @property
    def plan_progress(self) :
        if self.plan_is_active :
            _ratio = (timezone.now() - self.plan_start) / (self.plan_end - self.plan_start)   
            return int(_ratio * 100)
        else :
            return 0     

    @property
    def plan_earning(self) :
        if not self.plan :
            return 0.00
        else :
            #calcculate what the balance should be for the plan
            today = timezone.now()   
            diff = today - self.plan_start
            diff = diff.days 
            extra = (diff/self.plan.duration) * self.plan.get_interest(self.initial_balance)
            bal = self.initial_balance + extra
            if bal > self.expected_maximum_balance : bal = self.expected_maximum_balance
            return round(bal,2)
    
    @property
    def current_balance(self) :
        return  round(self.past_deposit_earning + self.plan_earning + self.funded_earning + self.referral_earning - self.withdrawals,2)


    
    @property
    def allowed_to_invest(self) :
        if self.plan :
            if self.plan_is_active :
                return False
        return True  

    def on_plan_complete(self)  :
        #deactivate plan
        self.plan_is_active = False
        past_earning = self.past_deposit_earning 
        self.past_deposit_earning = past_earning + self.plan_earning() + self.initial_balance
        self.previous_plan = self.plan
        self.initial_balance = 0.0
        self.plan = None
        self.plan_start = None
        self.plan_end = None
        self.save()

                    

    
    def __str__(self) :
        return self.user.username


    def save(self,*args,**kwargs) :
        super(Wallet,self).save(*args,**kwargs)     



class Transaction(models.Model) :
    
    def get_transaction_id(self) :
        PREFIX = "TD"
        number = random.randrange(10000000,999999999)
        number = PREFIX + str(number)
        if Transaction.objects.filter(transaction_id  = number).exists() : 
            self.get_transaction_id()
        return number

    status = (('Approved','Approved'),('Declined','Declined'),('Pending','Pending'))
    t_choices = (('WITHDRAWAL','WITHDRAWAL'),('DEPOSIT','DEPOSIT'),("BONUS","BONUS"),("AIR DROP","AIR DROP"),("REFERAL EARNING","REFERAL EARNING"))
    transaction_id = models.CharField(max_length=15,editable = False)
    user  = models.ForeignKey(get_user_model(),on_delete = models.CASCADE,related_name = 'user_transaction')
    transaction_type = models.CharField(max_length=20,choices = t_choices)
    description = models.TextField()
    status = models.CharField(max_length=10,choices = status,default = 'Pending')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(null = False)
    coin = models.CharField(blank = True,null = True,max_length=10)

    def __str__(self) :
        return self.transaction_id

    
    def save(self,*args,**kwargs) :
        if not self.transaction_id :
            self.transaction_id = self.get_transaction_id()   
        super(Transaction,self).save(*args,**kwargs)  

    class Meta() :
        ordering  = ['-date']      




class PendingDeposit(models.Model)    :
    user  = models.OneToOneField(get_user_model(),on_delete = models.CASCADE,related_name = 'user_pending_deposit')
    plan = models.ForeignKey(Plan,related_name = 'pending_deposit',null = True,on_delete = models.SET_NULL)
    amount = models.PositiveIntegerField(null = False)
    is_approved  = models.BooleanField(default = False)
    is_declined = models.BooleanField(default = False)
    #reason for declining
    decline_reason = models.TextField(null = True)
    coin = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
   


    def  __str__(self) :
        return self.user.username


    def save(self,*args,**kwargs) :
        super(PendingDeposit,self).save(*args,**kwargs)    




class WithdrawalApplication(models.Model) :
    coin_choices = (('BTC','BTC'),('USDT','USDT'),('ETH','ETH'),('BNB','BNB'))
    status = (('PENDING','PENDING'),('PROCESSING','PROCESSING'),('APPROVED','APPROVED'),('DECLINED','DECLINED'))
    user  = models.OneToOneField(get_user_model(),on_delete = models.CASCADE,related_name = 'pending_withdrawal')
    amount = models.FloatField()  #in $
    coin = models.CharField(max_length=10,choices = coin_choices)
    wallet_address = models.CharField(max_length= 200,help_text = "Please enter the correct address matching the selected coin,as any mismatch might lead to complete loss")
    #extra address info goes here
    status = models.CharField(max_length= 20,choices = status,default = 'PENDING')
    amount_paid = models.FloatField(blank = True,null = True)  
    is_received = models.BooleanField(default = True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.user.username

    def save(self,*args,**kwargs) :
        super(WithdrawalApplication,self).save(*args,**kwargs)         
    

 