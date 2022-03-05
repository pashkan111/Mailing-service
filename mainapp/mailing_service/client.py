import requests
from typing import List
from utils.logger import get_logger
from service.settings import env
import json


logger = get_logger(__name__)

class ServiceClient:
    """
    Client to interact with remote service
        which can send message to phone number
    """
    
    def __init__(self, data: List[dict]):
        service_url = env('SERVICE_URL')
        service_token = env('SERVICE_TOKEN')
        if service_url and service_token:
            self.url = service_url
            self.token = service_token
            self.data = data
        else:
            logger.error('Can not import service_url or service_token')
        
    def _get_url(self, obj: dict) -> str:
        try:
            id = obj['id']
            return f'{self.url}/{id}'
        except KeyError as e:
            logger.error(str(e))
    
    def send_data(self) -> dict:
        """
        Iterates by list of data objects and send data
        to mailing service
        Dict "results" contains info about clients who got the message
        """
        results = {}
        for obj in self.data:
            url = self._get_url(obj)
            json_data = json.dumps(obj)
            response = requests.post(
                url=url,
                data=json_data,
                headers={'Authorization': self.token}
            )
            client_phone = obj["phone"]
            try:
                response.raise_for_status()
                logger.info(
                    f'Message for client with phone {client_phone} has been sent'
                )
                results.setdefault(client_phone, True)
            except Exception:
                logger.error(
                    f'Error while delivering message for client with phone {client_phone}'
                )
                results.setdefault(client_phone, False)
        
        return results
        