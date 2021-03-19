import json
import requests
from urllib.parse import urlencode

debug = False

# Abstract class for handling api calls and responses
class Client():  
    def logger (self, *args):
        print(args)

    def api(self, path, method='get', params=None, data=None, query=None):
        final_url = self.BASE_URL + path
        final_params = {}
        if (params is not None):
            for key, value in params.items():
                if isinstance(value, list): 
                    final_params[key] = ','.join(value)
                else:
                    final_params[key] = value

        if (query is not None):
            final_url += '?'
            for key, value in query.items():
                # if isinstance(value, list): 
                    url_add =  '&'+ str(key) + '=' + str(value)
                    final_url += url_add
                # else:
                    # final_params[key] = value

        req = requests.Request(method.upper(), final_url, params=final_params)
        prepared = req.prepare()

        if debug is True:
            print('{}\n{}\r\n{}\r\n\r\n{}'.format(
                '-----------FINAL QUERY-----------',
                prepared.method + ' ' + prepared.url,
                '\r\n'.join('{}: {}'.format(k, v) for k, v in prepared.headers.items()),
                prepared.body,
            ))
        if (data is not None and debug is True):
            self.logger('data', json.dumps(data, indent=2))
        
        if method == 'get':
            response = requests.get(final_url, params=final_params)
        elif method == 'put':
            response = requests.put(final_url, params=final_params, data=data)
        elif method == 'post':
            response = requests.post(final_url, params=final_params, data=data)
        
        if response.status_code == 200:
            if debug is True:
                self.logger('response', response.content.decode('utf-8'))
            return json.loads(response.content.decode('utf-8')) # result returned as a json object
        elif debug is True:
            self.logger('an error occured for request:', method, final_url)
            self.logger(response.status_code, response.content)