from django import forms
from .models import WithdrawalApplication


class WithdrawalForm(forms.ModelForm) :

    def __init__(self,*args,**kwargs) :
        super(WithdrawalForm,self).__init__(*args,**kwargs)
        #self.fields['amount'].disabled = True                           

    
    class Meta() :
        model = WithdrawalApplication
        fields = ['coin','wallet_address','amount']


    def clean_amount(self) :
        amt = self.cleaned_data['amount'] 
        initial = getattr(self,'instance',None)
        return initial.amount or amt


class AmountForm(forms.Form)  :

    def __init__(self,plan = None,*args,**kwargs) :
        super().__init__(*args,**kwargs)
        self.plan = plan
    
    amount = forms.IntegerField()    


    def clean_amount(self) :
        amount  = self.cleaned_data['amount']
        if not self.plan : raise forms.ValidationError("An unspecified error occured,please try again later")
        if self.plan.max_cost and not amount <= self.plan.max_cost :
            raise forms.ValidationError("Amount must be the specified limits or select another plan") 
        if  not amount >=  self.plan.min_cost  :
            raise forms.ValidationError("Amount must be the specified limits or select another plan") 
        return amount