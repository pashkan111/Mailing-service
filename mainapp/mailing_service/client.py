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
    
    def send_data(self) -> bool:
        """
        Iterates by list of data objects and send data
        to service
        """
        for obj in self.data:
            url = self._get_url(obj)
            json_data = json.dumps(obj)
            response = requests.post(
                url=url,
                data=json_data,
                headers={'Authorization': self.token}
            )
            try:
                response.raise_for_status()
                result = response.json()
                logger.info('Data has been sent')
                logger.info(result)
                return True
            except Exception as e:
                logger.error(str(e))
                return False