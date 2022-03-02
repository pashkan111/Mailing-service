import os, requests


class ServiceClient:
    """
    Client to interact with remote service
        which can send message to phone number
    """
    
    def __init__(self):
        service_url = os.environ.get('SERVICE_URL')
        service_token = os.environ.get('SERVICE_TOKEN')
        data = data.get('id')
        if service_url and service_token and message_id:
            self.url = f'{service_url}/{message_id}'
            self.token = service_token
            self.data = data
        else:
            # add logging
            raise Exception
    
    def _get_data(self):
        try:
            phone = self.data['phone']
            text = self.data['text']
            self.data = {
                "id": id,
                "text": text,
                "phone": phone
            }
        except KeyError as e:
            # add logging
            raise Exception
    
    def send_data(self) -> bool:
        response = requests.post(
            url=self.url, 
            data=self.data,
            headers={'Authorization': self.token}
        )
        try:
            response.raise_for_status()
            return True
        except Exception as e:
            # add logging
            print(str(e))
            return False
        