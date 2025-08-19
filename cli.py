#Only for manual testing, not necessary for AI (created to ensure NOAA client was working correctly)
from src.api_client import NOAAAPIClient
from src.utils import format_weather_data, get_weather_summary

def main():
    client=NOAAAPIClient()
    location_name=input("Enter city name: ")
    locations=client.get_locations(location_name)
    if not locations:
        print("Location not found")
        return
    print(f"\nFound {len(locations)} locations:")
    for i, loc in enumerate(locations, 1):
        print(f"{i}. {loc['name']} (ID: {loc['id']})")

    if len(locations)>1:
        while True:
            try:
                choice=int(input("\nEnter the number of your chosen location: "))
                if 1<=choice<=len(locations):
                    loc_id=locations[choice-1]['id']
                    break
                else:
                    print(f"Please enter a number between 1 and {len(locations)}")
            except ValueError:
                print("Please enter a valid number")
    else:
        loc_id=locations[0]['id']
    date=input("\nEnter date (YYYY-MM-DD): ")
    weather=client.get_weather_data(loc_id, date)
    metrics=format_weather_data(weather)
    print(f"\nWeather for {location_name} on {date}:")
    print(get_weather_summary(metrics))

if __name__ == "__main__":
    main()
