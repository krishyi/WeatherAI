def format_weather_data(weather_json): #used to process noaa api response into specific data
    if not weather_json or not isinstance(weather_json, dict) or 'results' not in weather_json: #validates input
        return None
    metrics = { #storages for data which will be measured
        'max_temp':None,
        'min_temp':None,
        'precipitation':None,
        'dates':set(),
        'unit':'metric'
    }
    max_temps=[] #temporary lists to collect values
    min_temps=[]
    precip_records=[]
    for record in weather_json.get('results', []): #Process weather records from NOAA
        try:
            date=record['date'][:10] #Get date
            metrics['dates'].add(date) #store important dates
            datatype=record['datatype'] #gets data and records it
            value=float(record['value']) #converts data into number
            if datatype=='TMAX': #stores Max temperatures
                max_temps.append(value)
            elif datatype=='TMIN': #stores Min temperatures
                min_temps.append(value)
            elif datatype=='PRCP': #stores precipitation data
                precip_records.append(value)
        except (KeyError, ValueError) as e:
            continue
    if max_temps:
        metrics['max_temp']=max(max_temps)
    if min_temps:
        metrics['min_temp']=min(min_temps)
    if precip_records:
        metrics['precipitation']=sum(precip_records)/len(precip_records) #divide so that correct precip data given
    metrics['dates']=set(sorted(list(metrics['dates'])))
    return metrics if metrics['dates'] else None

def get_weather_summary(metrics): #Creates a weather summary
    if not metrics:
        return "No weather data available"
    summary=[]
    if metrics['max_temp'] is not None and metrics['min_temp'] is not None: #Temperature data
        temp_text=f"Max: {metrics['max_temp']:.1f}°C, Min: {metrics['min_temp']:.1f}°C"
        summary.append(temp_text)
    if metrics['precipitation'] is not None: #Precipitation data
        precip_text=f"Precipitation: {metrics['precipitation']:.1f} mm"
        summary.append(precip_text)
    if metrics['dates']: #If there is date range it is presented
        date_range=f"Date range: {metrics['dates'][0]} to {metrics['dates'][-1]}"
        summary.append(date_range)
    return "\n".join(summary)

def format_realtime_data(observation_json): #Important for AI, processes realtime data
    if not observation_json or 'properties' not in observation_json:
        return None
    props=observation_json['properties'] #gets weather properties

    return { #stores important information the user may ask, such as temp, humidtiy, wind speed, conditions, etc.
        'temperature':props.get('temperature', {}).get('value'),
        'humidity':props.get('relativeHumidity', {}).get('value'),
        'wind_speed':props.get('windSpeed', {}).get('value'),
        'conditions':props.get('textDescription'),
        'timestamp':props.get('timestamp'),
        'unit': 'metric'  #API returns metric data
    }