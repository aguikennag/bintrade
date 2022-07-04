from django.core.exceptions import ObjectDoesNotExist


def core(request) :
    prepend = "https://" if request.is_secure() else "http://"
    host = request.get_host()
    #reg_link  = prepend + host + request.user.user_admin.reg_link
    ctx = {}

    ctx['liquidity'] = 53199180
    ctx['site_name_verbose'] = "Afflus Trade"
    ctx['site_name'] = "Afflus Trade"
    ctx['site_name_full'] = "Afflus Trade"
    ctx['support_email'] = "support@afflus-trade.com"
    ctx['site_email'] = "support@afflus-trade.com"
    ctx['site_phone'] = "+3594858"
    ctx['site_whatsapp_no'] = "+66658656fg6"
    ctx['site_address'] = "No 23 winston road new york"
    ctx['ltc_wallet_address'] = "Ld7quXs9UXyRqQnxFSqwTqkoiWMCotUGdK"
    ctx['usdt_bep20_wallet_address'] = "0x1aeeffb9bebfa454682db27ba57e3e6079c401b8"
    ctx['usdt_trc20_wallet_address'] =  "TR1BVAZHnW8PcEdjhXqx6Bc6AF3aTW7i1X"
    ctx['eth_wallet_address'] = "0x1aeeffb9bebfa454682db27ba57e3e6079c401b8"
    ctx['btc_wallet_address'] = "bc1qezcxsgzq8g7sjtzt8vpz90tzpdnwnyqvmsgk68"
    ctx['bnb_wallet_address'] = "0x1aeeffb9bebfa454682db27ba57e3e6079c401b8"
    
    return ctx  


    
        