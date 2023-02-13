import requests

class Geocoding():

    "https://api-ninjas.com/api/geocoding"

    def __init__(self):
        self.base_url = 'https://api.api-ninjas.com/v1/'
        self.key = "NIsgOXtwmjvIJXGekIRa9w==RMMfXMPV4mUISydg"

    def get_geo_info(self,city,state='',country=''):
        action = 'geocoding?city={}&state={}&country={}'.format(city,state,country)
        response = requests.get(self.base_url+action, headers={'X-Api-Key': self.key})
        geos = response.json()
        try:
            geo = geos[0]
            geo_city = geo['name']
            geo_lat = geo['latitude']
            geo_long = geo['longitude']
            geo_country = geo['country']
        except:
            geo_city = ''
            geo_lat = ''
            geo_long = ''
            geo_country = ''
        return geo_city,geo_lat,geo_long,geo_country