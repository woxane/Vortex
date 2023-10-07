import requests
import re

def Check(Proxy) :
    ProxyValidation = re.match(r'^https?://\S+:\d+$' , Proxy)
    if not ProxyValidation : 
        print("The structure of proxy isn't correct .\nThe correct way : http(s)://exmaple:example")
        exit()
    Proxies = {
            'http' : 'http://' + Proxy , 
            'https' : 'https://' + Proxy
            }

    Response = requests.get('http://www.google.com' , proxies = Proxies , timeout = 10)
    if Response.status_code == 200 : 
        return True

    return False
