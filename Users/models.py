from email.policy import default
from django.db import models
from django.contrib.auth.models   import AbstractUser
from django.utils.text import  slugify
from django.contrib.auth import get_user_model
from django.conf import settings

import os
import random



class Country(models.Model) :
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=5)

    def __str__(self) :
        return self.short_name




class User(AbstractUser) :
    
    def get_path(instance,filename) :
        filename = "{}.{}".format(instance.name,filename.split('.')[1])
        return "users/dp/{}".format(filename)
    
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length = 30,blank = False,null = False)
    picture = models.FileField(upload_to = get_path)
    referals = models.ManyToManyField('self',symmetrical=False,blank = True,related_name ="referee")
    referral_id  = models.CharField(max_length=10,blank = True,editable = False)
    admin = models.ForeignKey('self',null = True,related_name="users",editable = False,on_delete = models.SET_DEFAULT,default = '1')
    is_admin = models.BooleanField(default = False)
    country = models.ForeignKey(Country,on_delete = models.SET_NULL,null = True)
    email_verified = models.BooleanField(default= False)

    @property
    def unique_id(self) :
        return "NTDID{}".format(self.pk)

    @property
    def get_picture(self) :
        BASE_DIR = settings.STATIC_URL
        default_path = os.path.join(BASE_DIR,"user-dashboard/images/user-thumb-sm.png")
        if not self.picture :
            return default_path
        
        return self.picture.url    

    def __str__(self)  :
        return self.username

    def save(self,*args,**kwargs) :
        self.slug = slugify(self.name) 
        if not self.referral_id  : self.referral_id = random.randrange(999999,99999999999)
        super(User,self).save(*args,**kwargs)


class Dashboard(models.Model) :
    last_checked = models.DateTimeField()


class Settings(models.Model) :
    user = models.ForeignKey(get_user_model(),related_name='settings',on_delete = models.CASCADE)
    email_on_transaction = models.BooleanField(default=False)


class WalletAddress(models.Model)  :
    user = models.ForeignKey(get_user_model(),related_name = "wallet_address",on_delete = models.CASCADE)  
    btc_address = models.CharField(max_length=60)
    usdt_address = models.CharField(max_length=60)
    eth_address = models.CharField(max_length=60)



class KYC(models.Model) :
    user = models.ForeignKey(get_user_model(),related_name = 'kyc',on_delete = models.CASCADE)
    is_verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


class Notification(models.Model) :
    user = models.ForeignKey(User,related_name = 'notification',on_delete = models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

    class Meta() :
        ordering = ['-date']


class NewsLaterSubscriber(models.Model) :
    user = models.ForeignKey(User,related_name = 'news_subscibers',on_delete = models.CASCADE)

    def __str__(self)  :
        return self.email
