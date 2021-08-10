import requests
import settings

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings()

class Authentication:
    vmanage_host = settings.vmanage_host
    vmanage_port = settings.vmanage_port
    username = settings.vmanage_username
    password = settings.vmanage_password

    def __init__(self, vmanage_host=vmanage_host, vmanage_port=vmanage_port, username=username, password=password):
        self.vmanage_host = vmanage_host
        self.vmanage_port = vmanage_port
        self.jsessionid = self.get_jsessionid(vmanage_host, vmanage_port, username, password)
        self.token = self.get_token(vmanage_host, vmanage_port, self.jsessionid)
        
        if self.token != None:
            self.headers = {'Content-Type': 'application/json', 'Cookie': self.jsessionid, 'X-XSRF-TOKEN': self.token }
        else:
            self.headers = {'Content-Type': 'application/json', 'Cookie': self.jsessionid }


    def get_jsessionid(self, vmanage_host, vmanage_port, username, password):
        api = "/j_security_check"
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        url = base_url + api
        payload = {'j_username' : username, 'j_password' : password}

        response = requests.post(url=url, data=payload, verify=False)
        try:
            cookies = response.headers["Set-Cookie"]
            jsessionid = cookies.split(";")
            return(jsessionid[0])
        except:
            print("No valid JSESSION ID returned\n")
            exit()


    def get_token(self, vmanage_host, vmanage_port, jsessionid):
        headers = {'Cookie': jsessionid}
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        api = "/dataservice/client/token"
        url = base_url + api      
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return(response.text)
        else:
            return None

class API:

    base_url = "https://{}:{}/dataservice".format(settings.vmanage_host, settings.vmanage_port)

    def send_request(self, method, path, headers, payload):
        url = self.base_url + path
        response = requests.request(method, url, headers=headers, data=payload, verify=False)
        return response.json()