import os, requests
from typing import List


class ServiceClient:
    """
    Client to interact with remote service
        which can send message to phone number
    """
    
    def __init__(self, data: List[dict]):
        service_url = os.environ.get('SERVICE_URL')
        service_token = os.environ.get('SERVICE_TOKEN')
        if service_url and service_token:
            self.url = service_url
            self.token = service_token
            self.data = data
        else:
            # add logging
            raise Exception
        
    def _get_url(self, obj: dict) -> str:
        try:
            id = obj['id']
            return f'{self.url}/{id}'
        except KeyError as e:
            # add logging
            print(str(e))
    
    def send_data(self) -> bool:
        """
        Iterates by list of data objects and send data
        to service
        """
        for obj in self.data:
            url = self._get_url(obj)
            response = requests.post(
                url=url,
                data=obj,
                headers={'Authorization': self.token}
            )
            try:
                response.raise_for_status()
                return True
            except Exception as e:
                # add logging
                print(str(e))
                return False
        