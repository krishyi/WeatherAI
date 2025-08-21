
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

