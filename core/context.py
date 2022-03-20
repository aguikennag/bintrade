from django.core.exceptions import ObjectDoesNotExist


def core(request) :
    prepend = "https://" if request.is_secure() else "http://"
    host = request.get_host()
    #reg_link  = prepend + host + request.user.user_admin.reg_link
    ctx = {}
    
    ctx['site_name_verbose'] = "Nintrend"
    ctx['site_name'] = "Nintrend"
    ctx['support_email'] = "support@nintrend.ltd"
    ctx['site_email'] = "support@nintrend.ltd"
    ctx['site_phone'] = "+3594858"
    ctx['site_whatsapp_no'] = "+66658656fg6"
    ctx['site_address'] = "No 23 winston road new york"
    ctx['ltc_wallet_address'] = "Ld7quXs9UXyRqQnxFSqwTqkoiWMCotUGdK"
    ctx['usdt_wallet_address'] = "0x1aeeffb9bebfa454682db27ba57e3e6079c401b8"
    ctx['eth_wallet_address'] = "0x1aeeffb9bebfa454682db27ba57e3e6079c401b8"
    ctx['btc_wallet_address'] = "12meM47zuwuzrBfRCm6KjrrJ5hDs1iZSD9"
    ctx['bnb_wallet_address'] = "0x1aeeffb9bebfa454682db27ba57e3e6079c401b8"
    
    return ctx  


    
        