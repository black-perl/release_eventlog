import os
from github_client import Github
from settings import USER,PASSWORD

class Release(object):
    '''
        The Release class.
        Represents the release flow for a user repo
    '''
    def __init__(self,user,repo):
        self._user = user # the owner of the repository
        self._repo = repo # the name of the repository
        self._client = Github(username=USER,
                              password=PASSWORD)

    def createRelease(self,options):
        '''
            Publish a release.
        '''
        endpoint = '/repos/{0}/{1}/releases'.format(self._user,self._repo)
        return self._client.post(endpoint,
                                 headers={},
                                 params={},
                                 payload=options)

    def uploadAsset(self,options):
        '''
            Upload assests to an earlier published release.
        '''
        headers = {}
        params = {}
        headers['Content-Type'] = 'application/vnd.debian.binary-package'

        if 'file_path' in options:
            file_path = options['file_path']
            if os.path.exists(file_path):
                data = open(file_path,'rb').read()
                params['name'] = file_path.split('/')[-1]
                if 'label' in options:
                    params['label'] = options['label']
            else:
                raise ValueError('Provided file_path does not exist.')
        else:
            raise ValueError('file_path is required')

        endpoint = 'repos/{0}/{1}/releases/{2}/assets'.format(self._user,self._repo,options['release_id'])
        self._client = Github(username=USER,password=PASSWORD,uploads=True)
        return self._client.post(endpoint,
                                 headers=headers,
                                 params=params,
                                 payload=data)


        