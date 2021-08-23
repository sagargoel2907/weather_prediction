import urllib3
import json
import datetime
http=urllib3.PoolManager()
try:
    response=http.request("GET","http://ipinfo.io/json")
    data=json.loads(response.data)
    #getting the latitute and longitude of the user location
    loc=data["loc"]
    loc=list(map(float,loc.split(",")))

    from pyowm.owm import OWM
    owm = OWM('e06f8937c85fbe26ca6a682282dfc57b')
    mgr = owm.weather_manager()
    present_day=datetime.datetime.now()
    week_day=datetime.datetime.weekday(present_day)
    week_days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    DEGREE_SYMBOL=u"\N{DEGREE SIGN}"

    #predicting for upcoming days based on current average weather in neighbouring cities
    for i in range(1,4):
        obs_list=mgr.weather_around_coords(*loc,limit=5*i)
        average_min_temperature=0
        average_max_temperature=0
        average_feels_like=0
        average_humidity=0
        detailed_status={}
        for observation in obs_list:
            #getting weather information like min-temp,max-temp,humidity etc for neighbouring cities
            weather=observation.weather
            temperature_data=weather.temperature(unit="celsius")
            average_min_temperature+=temperature_data['temp_min']
            average_max_temperature+=temperature_data['temp_max']
            average_feels_like+=temperature_data['feels_like']
            average_humidity+=weather.humidity
            status=weather.detailed_status
            if status in detailed_status:
                detailed_status[status]+=1
            else:
                detailed_status[status]=1

        #finding detailed status of each day based on most frequent status in neighbouring cities
        detailed_status=detailed_status.items()
        detailed_status=sorted(detailed_status,key=lambda t:t[1],reverse=True)

        average_min_temperature/=(5*i)
        average_min_temperature=round(average_min_temperature,1)
        average_max_temperature/=(5*i)
        average_max_temperature=round(average_max_temperature,1)
        average_humidity/=(5*i)
        average_humidity=round(average_humidity,1)
        average_feels_like/=(5*i)
        average_feels_like=round(average_feels_like,1)
        print("-"*30)
        print(f"{week_days[(week_day+i)%7]} Predicted Weather : \n\nMinimum Temperature : {average_min_temperature}{DEGREE_SYMBOL}C \nMaximum Temperature : {average_max_temperature}{DEGREE_SYMBOL}C\nFeels like : {average_feels_like}{DEGREE_SYMBOL}C")
        print(f"Predicted weather Type : {detailed_status[0][0]}")
        print(f"Humidity : {average_humidity}\n\n\n")
except:
    print("There is problem in connecting to the Internet.\nTry troubleshooting it and try again")



