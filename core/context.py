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
    ctx['site_phone'] = "+3594858454"
    ctx['site_whatsapp_no'] = "+66658656fg6"
    ctx['site_address'] = "No 23 winston road new york"
    ctx['ltc_wallet_address'] = "ltc1q3spehp5aeunwnf75pnj2ka4h4h207cks09vrfx"
    ctx['usdt_bep20_wallet_address'] = "0x23c6742837e45c2dcdd169b79d06eeeb6b108b9b"
    ctx['usdt_trc20_wallet_address'] =  "TNiQErvJZMrnXHDGRyaxu9ZeVAPixk98AX"
    ctx['eth_wallet_address'] = "0x35A3af01822B37FEb4f1E16319daAd1c208e0F9c"
    ctx['btc_wallet_address'] = "1MJZZuHVErPeEa87rhBC6MpJyp3zRuPyp9"
    ctx['bnb_wallet_address'] = "0x23c6742837e45c2dcdd169b79d06eeeb6b108b9b"
    
    return ctx  


    
        