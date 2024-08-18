from django.core.exceptions import ObjectDoesNotExist


def core(request) :
    prepend = "https://" if request.is_secure() else "http://"
    host = request.get_host()
    #reg_link  = prepend + host + request.user.user_admin.reg_link
    ctx = {}

    ctx['liquidity'] = 53199180
    ctx['site_name_verbose'] = "Bintrade"
    ctx['site_name'] = "Bintrade"
    ctx['site_name_full'] = "Bintrade"
    ctx['support_email'] = "support@zealkoin.ltd"
    ctx['site_email'] = "support@zealkoin.ltd"
    ctx['site_phone'] = ""
    ctx['site_whatsapp_no'] = ""
    ctx['site_address'] = "No 23 winston road new york"
    ctx['ltc_wallet_address'] = "ltc1qsvg0t9t6uehwawm0u6kgqtylxrnhctsey4q26e"
    ctx['usdt_trc20_wallet_address'] =  "TJsjwva9wgeAsu48qXCMoAVdWf3CfpjsrT"
    ctx['eth_wallet_address'] = "0xaFE97eeBDBD23940EB3c324887dbF3984A7A5B44"
    ctx['btc_wallet_address'] = "bc1q6q0yutnp6xzdw2qzzr36fvnvhd3ue26ezwregv"
    ctx['bnb_wallet_address'] = "bnb1tchrv3p808sv3zt0jgcu993qczfd42d3amzadn"
    
    return ctx  


    
        