from django.core.exceptions import ObjectDoesNotExist


def core(request) :
    prepend = "https://" if request.is_secure() else "http://"
    host = request.get_host()
    #reg_link  = prepend + host + request.user.user_admin.reg_link
    ctx = {}

    ctx['site_name'] = "Nintrend"
    ctx['support_email'] = "support@nintrend.ltd"
    ctx['site_email'] = "support@nintrend.ltd"
    ctx['site_phone'] = "+3594858"
    ctx['site_whatsapp_no'] = "+66658656fg6"
    ctx['site_address'] = "No 23 winston road new york"

    ctx['usdt_wallet_address'] = "udusfuvusuyusfdy8gg36g687"
    ctx['eth_wallet_address'] = "6t43btr7f6t6wtf76t463tr6tfr"
    ctx['btc_wallet_address'] = "8763g4yf668r76734fg7hu7b76v"
    ctx['ltc_wallet_address'] = "gurt8768w7ter67ew7gtrtfg7tt"
    
    return ctx  


    
        