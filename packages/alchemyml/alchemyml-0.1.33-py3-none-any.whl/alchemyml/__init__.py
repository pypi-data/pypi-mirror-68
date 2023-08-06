from ._version import __version__

__doc__ = '''
alchemyml - Automation of data lifecycle
========================================

**alchemyml** is a multi-environment tool for automating the data lifecycle 
and accelerating advanced data analysis processes. From data ingest and 
preparation, through pre-processing and up to the construction of predictive 
models, **alchemyml** provides the data scientist with aldata science applied 
artificial intelligence tools to optimize their work, time and resources. 
'''

class alchemyml():
    '''
    Main AlchemyML class containing all available classes and methods. To load 
    the token into the object is necessary to call "get_api_token" method, and 
    then all methods will be available through classes "dataset", "experiment", 
    "project" or "actions". 
    '''

    from ._CRUD_classes import dataset, experiment, project, authentication
    from ._manual_ops import actions

    def get_api_token(self, username, password):
        '''
        This method returns the necessary token to be used from now on for the 
        API requests. To be able to make use of the API before all it is 
        necessary to sign-up.

        Parameters:

        username (str): Username. 
        password (str): Password. 
        '''
        import json
        from ._request_handler import retry_session

        url = 'https://alchemyml.com/api/token/'
        data = json.dumps({'username':username, 'password':password})
        session = retry_session(retries = 10)
        r = session.post(url, data)
        session.close()

        if r.status_code == 200:
            tokenJSON = json.loads(r.text)
            self.dataset.token = tokenJSON['access']
            self.experiment.token = tokenJSON['access']
            self.project.token = tokenJSON['access']
            self.actions.token = tokenJSON['access']
            return tokenJSON['access']

        elif r.status_code == 404:
            return '404: Not Found'

        elif r.status_code == 500:
            return '500: Internal Server Error'

        elif r.status_code == 503:
            return '503: Service Unavailable'

        else:
            msgJSON = json.loads(r.text)
            return msgJSON['message']

