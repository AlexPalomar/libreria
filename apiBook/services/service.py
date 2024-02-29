import requests

class Service:

    def generate_request(self ,url, params={}):
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()

    def get_username(self, params={}):
        response = self.generate_request('https://randomuser.me/api', params)
        if response:
            user = response.get('results')[0]
            return user.get('name').get('first')

        return ''