import os, requests


class ServiceClient:
    """
    Client to interact with remote service
        which can send message to phone number
    """
    
    def __init__(self, id):
        service_url = os.environ.get('SERVICE_URL')
        service_token = os.environ.get('SERVICE_TOKEN')
        if service_url and service_token:
            self.url = f'{service_url}/{id}'
            self.token = service_token
        else:
            raise Exception
    
    def send_data(self, data: dict) -> bool:
        response = requests.post(
            url=self.url, 
            data=data,
            headers={'Authorization': self.token}
        )
        try:
            response.raise_for_status()
            return True
        except Exception as e:
            # add loging
            print(str(e))
            return False