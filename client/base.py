import base64
import json
import requests
from urlparse import urljoin

DEFAULT_HEADERS = {
    'User-Agent' : 'release_eventlog',
    'From' : 'black-perl.in',
    'Content-Type' : 'application/json'
}

TIMEOUT_SEC = 30


class APIError(StandardError):
    """
    APIError contains json message indicating failure
    """
    def __init__(self, error_id, error_message, error_name, request,  *args, **kwargs):
        self.error_id = error_id
        self.error_message = error_message
        self.error_name = error_name
        self.request = request
        super(StandardError, self).__init__(*args, **kwargs)

    def __str__(self):
        return super(StandardError, self).__str__() + '\n' \
        'APIError: %s: %s\n%s\nURL: %s' % \
        (self.error_id,self.error_name, self.error_message, self.request)


class Result(object):
    '''
        Parse the result of the request and check for errors
    '''
    def __init__(self,result,request_url):
        self._request_url = request_url
        self._responseHeaders = {}
        self._status = result.status_code
        self._json = None
        try:
            self._json = json.loads(result.text)
            self._responseHeaders = result.headers

        except ValueError as e:
            raise APIError('ValueError', 
                           result.text, 
                           'ValueError', 
                           request_url, 
                           e)

        if 'error_id' in result:
            raise APIError(result['error_id'], 
                           result['error_message'],
                           result['error_name'], 
                           request_url)

        if 'message' in result:
            if 'rate limit exceeded' in result['message']:
                raise APIError('Rate limit exceeded', 
                               result['message'],
                               'Rate limit exceeded', 
                               request_url)

    @property
    def headers(self):
        return self._responseHeaders

    @property
    def json(self):
        return self._json

    @property 
    def request_url(self):
        return self._request_url

    @property
    def status(self):
        return self._status

    def __str__(self):
        return "Result instance - {0}".format(self._status)


class BaseClient(object):
    '''
    The Base Client class that handles request object composition.
    '''
    http_methods = (
        'head',
        'get',
        'post',
        'put',
        'patch',
        'delete',
        )

    def __init__(self,endpoint=None,username=None,password=None):
        '''
            Instantiate a Generic Client
        '''
        self._endpoint = endpoint
        self._username = username
        self._password = password
        self._headers = DEFAULT_HEADERS
        self.authorizeRequest()

    def encodeCredentials(self):
        '''
            Returns the base64 encoded auth string for doing Basic Authorization.
            The method is called in a fail-safe way, i.e pre-checking username and passwords.
        '''
        return base64.b64encode(self._username + ':' + self._password)

    def authorizeRequest(self):
        '''
            Generate and add authorization headers
        '''
        if self._username is not None:
            if self._password is None:
                raise TypeError("You need a password to authenticate as " + self._username)
            else:
                self._headers['Authorization'] = 'Basic ' + self.encodeCredentials()
        else:
            # No authorization is required 
            pass

    def makeRequest(self,method='get',url='',headers={},params={},payload={}):
        '''
            Carry out a request
        '''
        method = method.lower()
        methodToCall = getattr(requests,method)
        request_url = urljoin(self._endpoint,url)
        self._headers.update(headers)
        headers = self._headers
        try:
            if method == 'post' or method == 'put':
                if headers['Content-Type'] == 'application/json':
                    data = json.dumps(payload)
                else:
                    data = payload
                result = methodToCall(request_url,
                                      headers=headers,
                                      params=params,
                                      data=data,
                                      timeout=TIMEOUT_SEC)
            else:
                result = methodToCall(request_url,
                                      headers=headers,
                                      params=params,
                                      data=payload,
                                      timeout=TIMEOUT_SEC)


        except requests.exceptions.ConnectionError as e:
            raise APIError('ConnectionError', 
                           'ConnectionError', 
                           'ConnectionError',
                           request_url, 
                           e)

        except requests.exceptions.Timeout as te:
            raise APIError('Timeout', 
                           'Timeout', 
                           'Timeout', 
                           request_url, 
                           te)

        except requests.exceptions.RequestException as re:
            raise APIError('RequestException', 
                           'RequestException', 
                           'RequestException', 
                           request_url, 
                           re)

        return Result(result,request_url)

    def get(self,url='',headers={},params={}):
        '''
            Do a GET request
        '''
        return self.makeRequest('get',url,headers,params)

    def head(self,url='',headers={},params={}):
        '''
            Do a HEAD request
        '''
        return self.makeRequest('head',url,headers,params)

    def post(self,url='',headers={},params={},payload={}):
        '''
            Do a POST request
        '''
        return self.makeRequest('post',url,headers,params,payload)

    def put(self,url='',headers={},params={},payload={}):
        '''
            Do a PUT request
        '''
        return self.makeRequest('put',url,headers,params,payload)

    def delete(self,url='',headers={},params={}):
        '''
            Do a DELETE request
        '''
        return self.makeRequest('delete',url,headers,params)
