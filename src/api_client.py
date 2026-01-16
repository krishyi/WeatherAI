import requests
from src.config import Config

class NOAAAPIClient:
    def __init__(self):
        Config.validate()
        self.base_url = Config.NOAA_BASE_URL #api website
        self.headers = {"token": Config.NOAA_API_TOKEN} #uses api token

        #stores common city names
        self.known_locations = {
            'seattle': 'CITY:US530014',
            'boston': 'CITY:US250017',
            'chicago': 'CITY:US170616',
            'miami': 'CITY:US120994',
            'new york': 'CITY:US360019',
            'los angeles': 'CITY:US060037',
            'denver': 'CITY:US080018',
            'atlanta': 'CITY:US130022',
        }

    def get_available_datasets(self): #gets list of available weather datasets from NOAA
        try:
            response = requests.get(
                f"{self.base_url}datasets", #address for the datasets
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e: #error handling
            print(f"Error getting datasets: {e}")
            return []

    def get_weather_data(self, location_id, start_date, end_date=None): #gets data from NOAA for a specific location and date/date range
        end_date = end_date if end_date else start_date

        params = {
            'datasetid': 'GHCND', #Global Historical Climatology Network Daily
            'locationid': location_id,
            'startdate': start_date,
            'enddate': end_date,
            'units': 'metric', #metric units are used
            'datatypeid': 'TMAX,TMIN,PRCP', #temp max, min, precip
            'limit': 1000
        }

        try: #debugging prompts printed to display what is being done within the program based on the user req, helpful for debugging errors
            print(f"Making NOAA API request with params: {params}")
            response=requests.get(
                f"{self.base_url}data",
                params=params,
                headers=self.headers,
                timeout=15
            )
            print(f"NOAA API response status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"NOAA API returned {len(data.get('results', []))} records")
                return data
            else:
                print(f"NOAA API error: {response.text}")
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def get_locations(self, city_name): #gets the location, incase a location is mentioned by the user
        city_lower = city_name.lower().strip()

        #checks if the city is from the list database
        if city_lower in self.known_locations:
            location_id = self.known_locations[city_lower]
            print(f"Using known location ID for {city_name}: {location_id}")
            return [{'id': location_id, 'name': city_name.title()}]

        #searches for location via api
        try:
            print(f"Searching NOAA API for locations matching '{city_name}'")

            response = requests.get(
                f"{self.base_url}locations",
                headers=self.headers,
                params={
                    'locationcategoryid': 'CITY',
                    'sortfield': 'name',
                    'sortorder': 'asc',
                    'limit': 1000
                },
                timeout=10
            )

            if response.status_code!=200:
                print(f"DEBUG: Location API returned status {response.status_code}: {response.text}")
                return []
            all_locations=response.json().get('results', [])
            print(f"DEBUG: Retrieved {len(all_locations)} total locations from API")
            city_upper = city_name.upper()
            matched = []

            for loc in all_locations:
                loc_name = loc['name'].upper()
                if (city_upper in loc_name or
                        any(city_upper in word for word in loc_name.split()) or
                        any(word.startswith(city_upper) for word in loc_name.split(','))):
                    matched.append(loc)

            print(f"DEBUG: Found {len(matched)} matching locations via API")
            return matched

        except Exception as e:
            print(f"Location search error: {str(e)}")
            return []
