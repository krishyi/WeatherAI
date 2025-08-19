import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NOAA_API_TOKEN=os.getenv("NOAA_API_TOKEN")
    NOAA_BASE_URL="https://www.ncdc.noaa.gov/cdo-web/api/v2/"

    @classmethod
    def validate(cls):
        if not cls.NOAA_API_TOKEN:
            print("Error: Missing API Token")
            exit(1)