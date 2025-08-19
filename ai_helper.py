import ollama
from src.api_client import NOAAAPIClient
from src.utils import format_weather_data
import re

class WeatherAI:
    def __init__(self):
        self.client=NOAAAPIClient() #sets up noaa client and ai model
        self.model="mistral" #confirms that mistral is used
        self.conversation_history=[] #stores history

    def extract_info(self, query): #This will tell the AI what information is needed, determining data such as the date and location
        prompt=f"""
        Extracts location and date from query:
        "{query}"
        Responds in this JSON format:
        {{"location": "city name or null", "date": "YYYY-MM-DD or null"}}
        """
        try: #Asks the AI to find the location and date in the question, and instructs it to use the JSON format
            response=ollama.generate(model=self.model, prompt=prompt, format='json')
            return response
        except Exception as e: #error handling
            print(f"Error extracting info: {e}")
            return {"location": None, "date": None}

    def generate_response(self, query): #Generates an intelligent response based on query
        #Checks if user has mentioned a location or a date
        info=self.extract_info(query)
        location=info.get('location')
        date=info.get('date')

        #Determines if weather data can be retrieved to fit the users prompt
        noaa_context=""
        if location and date:
            weather=self.client.get_weather_data(location, date)
            metrics=format_weather_data(weather)
            noaa_context=f"NOAA weather data: {metrics}" if metrics else ""

        #Prepares answer for the user, if data is available, comments used to demonstrate the AI's logic
        if noaa_context:
            prompt = f"""
            [ROLE] You're a meteorologist with access to NOAA data.
            [DATA] {noaa_context}
            [QUESTION] {query}
            Answer using the data when possible, supplement with your knowledge.
            """
        else: #Provides a detailed answer even if exact data is not available, using estimates
            prompt = f""" 
            [ROLE] You're a weather expert.
            [QUESTION] {query}
            Provide a detailed, scientific answer about weather patterns.
            """
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']

    def chat_interface(self):
        print("Weather AI (type 'quit' to exit)\n") #Prints a basic prompt with examples for the user to input
        print("You can ask questions such as:")
        print("- Explain how hurricanes form")
        print("- Was it rainy in Seattle on May 15, 2021?")
        print("- Compare summer temperatures in Chicago and Miami\n")

        while True: #continues chatting until the user quits
            query=input("\nYour weather question: ").strip()
            if query.lower() in ['quit', 'exit']:
                break
            if not query:
                continue
            response=self.generate_response(query) #Produces AI responsee and prints it
            print("\nAI Response:")
            print(response)


if __name__ == "__main__":
    ai = WeatherAI()

    ai.chat_interface()


