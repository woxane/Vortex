import requests

def Check(Proxy) : 
    Proxies = {
            'http' : 'http://' + Proxy , 
            'https' : 'https://' + Proxy
            }

    Response = requests.get('http://www.google.com' , proxies = Proxies , timeout = 10)
    if Response.status_code == 200 : 
        return True

    return False
