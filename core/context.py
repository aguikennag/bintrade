from django.core.exceptions import ObjectDoesNotExist


def core(request) :
    prepend = "https://" if request.is_secure() else "http://"
    host = request.get_host()
    #reg_link  = prepend + host + request.user.user_admin.reg_link
    ctx = {}

    ctx['site_name'] = "Nintrend"
    ctx['site_email'] = "support@nintrend.ltd"
    ctx['site_phone'] = "+3594858"
    ctx['site_whatsapp_no'] = "+66658656fg6"
    ctx['site_address'] = "No 23 winston road new york"

    ctx['usdt_wallet_address'] = "GUYDgfuygsuyfsdygryfrr"
    ctx['eth_wallet_address'] = "GUYDgfuygsuyfsdygryfrr"
    ctx['btc_wallet_address'] = "GUYDgfuygsuyfsdygryfrr"
    return ctx  


    
        