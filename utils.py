#This will process the NOAA API response into readable weather metrics
def format_weather_data(weather_json):
    #validates that correct data is being received from NOAA
    if not weather_json or not isinstance(weather_json, dict) or 'results' not in weather_json:
        print("Invalid weather data structure")
        return None
    #gets weather results from noaa
    results = weather_json.get('results', [])
    if not results:
        print("No results in weather data")
        return None

    print(f"Processing {len(results)} weather records")

    metrics ={ #data structure to process weather data
        'max_temp': None,
        'min_temp': None,
        'precipitation': None,
        'dates': set(),
        'unit': 'metric'
    }
    #temp lists to collect temp and precip values
    max_temps=[]
    min_temps=[]
    precip_records=[]

    #goes through each record from noaa to extract the necessary data
    for record in results:
        try:
            date=record['date'][:10]  #extract YYYY-MM-DD
            metrics['dates'].add(date) #keeps track of dates
            datatype=record['datatype'] #tmax tmin prcp
            value=float(record['value']) #store measurements
            print(f"Record - Date: {date}, Type: {datatype}, Value: {value}")

            #sorts data by diff types
            if datatype=='TMAX':
                max_temps.append(value)
            elif datatype=='TMIN':
                min_temps.append(value)
            elif datatype=='PRCP':
                precip_records.append(value)

        except (KeyError, ValueError, TypeError) as e:
            print(f"Skipping invalid record: {e}")
            continue

    #Calculate final summary statistics
    if max_temps:
        metrics['max_temp']=max(max_temps)
    if min_temps:
        metrics['min_temp']=min(min_temps)
    if precip_records:
        metrics['precipitation']=sum(precip_records)  #Total precipitation

    #converts dates to sorted list
    metrics['dates']=sorted(list(metrics['dates']))
    print(f"Final metrics: {metrics}")

    #return metrics if we have at least some data
    if metrics['dates'] and (metrics['max_temp'] is not None or
                            metrics['min_temp'] is not None or
                            metrics['precipitation'] is not None):
        return metrics
    print("No valid metrics found")
    return None
