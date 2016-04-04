from client import BaseClient

API_ENDPOINT = 'https://api.github.com'
UPLOAD_ENDPOINT = 'https://uploads.github.com'

class Github(BaseClient):
    '''
        Github client
    '''
    def __init__(self,username=None,password=None,uploads=False):
        if not uploads:
            super(Github,self).__init__(endpoint=API_ENDPOINT,
                                        username=username,
                                        password=password)
        else:
            super(Github,self).__init__(endpoint=UPLOAD_ENDPOINT,
                                        username=username,
                                        password=password)

        extra_headers = {
            'accept' : 'application/vnd.github.v3+json'
        }
        self._headers.update(extra_headers)



