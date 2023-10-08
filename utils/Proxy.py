import requests
import re

def Check(Proxy) :
    ProxyValidation = re.match(r'^https?://\S+:\d+$' , Proxy)
    if not ProxyValidation : 
        print("The structure of proxy isn't correct .\nThe correct way : http(s)://exmaple:example")
        exit()
    Proxies = {
            'http' : Proxy , 
            'https' :  Proxy
            }

    try : 
        Response = requests.get('http://www.google.com' , proxies = Proxies )

    except Exception as Excep : 
        print('your proxy is failed . ')
        print('exiting ... ')
        exit()
