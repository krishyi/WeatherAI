import requests
from src.config import Config

class NOAAAPIClient:
    def __init__(self):
        Config.validate() #check if config valid
        self.base_url=Config.NOAA_BASE_URL #api website
        self.headers={"token":Config.NOAA_API_TOKEN} #pass for noaa
        self.realtime_url = "https://api.weather.gov/"
    def get_available_datasets(self): #Ask NOAA's server for a list of datasets
        response=requests.get(
            f"{self.base_url}datasets", #address for datasets
            headers=self.headers,
            timeout=10
        )
        return response.json().get('results', []) #gets the list
    def get_weather_data(self, location, start, end=None):
        end=end if end else start #if there is no end date, use start date
        params={
            'datasetid':'GHCND', #global historical climatology network data
            'locationid':location, #location id
            'startdate':start,
            'enddate':end, #creates date range, if range is used
            'units':'metric', #confirms metric units used
            'datatypeid':['TMAX', 'TMIN', 'PRCP'], #temp max/min, precipitation
            'limit':1000 #limits records
        }
        try:
            request_params=params.copy() #create copy of params so original unchanged
            request_params['datatypeid']=','.join(params['datatypeid']) #convert datatype list to string for api
            response=requests.get( #makes request to noaa for data
                f"{self.base_url}data", #api data
                params=request_params,
                headers=self.headers, #auth header
                timeout=10
            )
            response.raise_for_status()
            return response.json() #return parsed json response
        except requests.exceptions.RequestException as e: #if there is error req data, error is logged and none is returned
            print(f"Error fetching data: {e}")
            return None

    def get_locations(self, name): #searches for locations by matching to names
        try:
            response=requests.get( #sends req using city name
                f"{self.base_url}locations", #api data of locations
                headers=self.headers,
                params={
                    'locationcategoryid': 'CITY', #categorizes as city
                    'sortfield': 'name', #sorts city names
                    'sortorder': 'asc', #creates order of cities
                    'limit': 1000 #max that api searches from a user input
                },
                timeout=10
            )
            response.raise_for_status() #check for errors
            matched=[
                loc for loc in response.json().get('results', [])
                if name.upper() in loc['name'].upper() #if theres is full match
                   or any(name.upper() in word for word in loc['name'].split()) #if there is partial match
            ]
            return matched #the matched locations are returned

        except Exception as e:
            print(f"Location search error: {str(e)}") #if no location, error is logged
            return None
