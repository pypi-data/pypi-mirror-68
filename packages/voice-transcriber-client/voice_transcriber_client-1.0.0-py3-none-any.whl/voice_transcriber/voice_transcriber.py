import os

import requests


class VoiceTranscriber:
    def __init__(self, domain, api_key):
        self.domain = domain
        self.api_key = api_key

    def transcribe(self, name, filename):
        file_ext = os.path.splitext(filename)[1]
        data = {"name": name + file_ext}
        request = requests.post('https://{}/recordings'.format(self.domain), headers=self.__headers(), json=data)

        if request.status_code == 200:
            response = request.json()
            upload_url = response['upload_url']
            request = requests.put(upload_url, headers=self.__headers(), data=open(filename, 'rb').read())
            return request.status_code == 200

        raise RuntimeError('An unexpected error occurred')

    def __headers(self):
        return {
            'x-api-key': self.api_key
        }
