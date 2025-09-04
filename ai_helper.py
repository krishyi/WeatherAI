import ollama
from src.api_client import NOAAAPIClient
from src.utils import format_weather_data
import json

class WeatherAI:
    def __init__(self):
        self.client=NOAAAPIClient()
        self.model="mistral"
        self.conversation_history=[]

    def extract_info(self, query):
        prompt=f'Extract location and date from "{query}". Return JSON: {{"location": "city or null", "date": "YYYY-MM-DD or null"}}'
        try:
            response=ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            content=response['message']['content'].strip()

            #clean up the response to extract JSON
            if '```' in content:
                # extract from code blocks
                parts=content.split('```')
                for part in parts:
                    part=part.strip()
                    if part.startswith('json'):
                        content=part[4:].strip()
                        break
                    elif part.startswith('{'):
                        content=part
                        break

            #remove any leading text before the JSON
            if not content.startswith('{'):
                json_start=content.find('{')
                if json_start!=-1:
                    content=content[json_start:]

            result=json.loads(content)

            #validates the result
            if not isinstance(result, dict):
                raise ValueError("Result is not a dictionary")

            #ensures we have the expected keys with proper null handling
            location=result.get('location')
            date=result.get('date')

            #converts null to none
            if location=="null" or location=="":
                location=None
            if date=="null" or date=="":
                date=None

            print(f"Extracted location='{location}', date='{date}'")
            return {"location": location, "date": date}

        except Exception as e:
            print(f"Error extracting info: {e}")
            print(f"Raw response was: {content if 'content' in locals() else 'No content'}")
            return {"location": None, "date": None}

    def generate_response(self, query):
        print(f"Processing query: '{query}'")

        #extract location and date information
        info=self.extract_info(query)
        location_name=info.get('location')
        date=info.get('date')

        print(f"Extracted info - Location: {location_name}, Date: {date}")

        noaa_context=""
        if location_name and date:
            print(f"Searching for locations matching '{location_name}'")

            # gets proper location ID from NOAA
            locations=self.client.get_locations(location_name)

            if locations:
                location_id=locations[0]['id']
                location_display=locations[0]['name']
                print(f"Found location: {location_display} (ID: {location_id})")

                #Gets weather data from NOAA
                print(f"Fetching weather data for {location_id} on {date}")
                weather=self.client.get_weather_data(location_id, date)

                if weather:
                    print(f"Raw weather data received: {len(weather.get('results', []))} records")
                    metrics=format_weather_data(weather)
                    if metrics:
                        print(f"Formatted metrics: {metrics}")
                        noaa_context=f"NOAA weather data for {location_display} on {date}: {metrics}"
                    else:
                        print("No metrics after formatting")
                else:
                    print("No weather data received from NOAA")
            else:
                print(f"No locations found for '{location_name}'")

        #based on the data the ai generates a response
        if noaa_context:
            prompt=f"You're a meteorologist. Use this data to answer: {noaa_context} Question: {query}"
        else:
            prompt=f"You're a weather expert for: {query}"

        print("Generating AI response...")
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']

    def chat_interface(self):
        print("Weather AI (type 'quit' to exit)\n")
        print("You can ask questions such as:")
        print("- Explain how hurricanes form")
        print("- Was it rainy in Seattle on May 15, 2024?")
        print("- Compare summer temperatures in Chicago and Miami\n")

        while True:
            query=input("\nYour weather question: ").strip()
            if query.lower() in ['quit', 'exit']:
                break
            if not query:
                continue

            response=self.generate_response(query)
            print("\nAI Response:")
            print(response)


if __name__ == "__main__":
    ai = WeatherAI()
    ai.chat_interface()




