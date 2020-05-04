from threading import Thread
import copy

database = {
    # Ort
    (12.3, 23.2): {
        "data": {
            "astronomy": {
                "sun_set": [283748323],
                "sun_rise": [897634534],
                "moon_set": [8234432278],
                "moon_rise": [237487823]
            },
            "weather": {
                (1588436500, 1588436560): {
                    "temperature_real": 32,
                    "temperature_felt": 50,
                    "humidity": 20,
                    "pressure": 1000,
                    "wind_speed": 10,
                    "wind_direction": 310,
                    "wind_direction_code": "NW",
                    "wind_direction_name": "North West",
                    "clouds_name": "covered",
                    "view_distance": 10000,
                    "precipitation": "none",
                    "weather_name": "cloudy",
                    "source": "OpenWeatherMap"
                },
                (1588436540, 1588436600): {
                    "temperature_real": 36,
                    "temperature_felt": 51,
                    "humidity": 20,
                    "pressure": 1000,
                    "wind_speed": 10,
                    "wind_direction": 310,
                    "wind_direction_code": "NW",
                    "wind_direction_name": "North West",
                    "clouds_name": "covered",
                    "view_distance": 10000,
                    "precipitation": "none",
                    "weather_name": "cloudy",
                    "source": "OpenWeatherMap"
                },
                (1588436620, 1588436680): {
                    "temperature_real": 34,
                    "temperature_felt": 52,
                    "humidity": 20,
                    "pressure": 1000,
                    "wind_speed": 10,
                    "wind_direction": 310,
                    "wind_direction_code": "NW",
                    "wind_direction_name": "North West",
                    "clouds_name": "covered",
                    "view_distance": 10000,
                    "precipitation": "none",
                    "weather_name": "cloudy",
                    "source": "OpenWeatherMap"
                },
                (1588436780, 1588436840): {
                    "temperature_real": 35,
                    "temperature_felt": 53,
                    "humidity": 20,
                    "pressure": 1000,
                    "wind_speed": 10,
                    "wind_direction": 310,
                    "wind_direction_code": "NW",
                    "wind_direction_name": "North West",
                    "clouds_name": "covered",
                    "view_distance": 10000,
                    "precipitation": "none",
                    "weather_name": "cloudy",
                    "source": "OpenWeatherMap"
                },
                (1588436740, 1588436800): {
                    "temperature_real": 36,
                    "temperature_felt": 54,
                    "humidity": 20,
                    "pressure": 1000,
                    "wind_speed": 10,
                    "wind_direction": 310,
                    "wind_direction_code": "NW",
                    "wind_direction_name": "North West",
                    "clouds_name": "covered",
                    "view_distance": 10000,
                    "precipitation": "none",
                    "weather_name": "cloudy",
                    "source": "OpenWeatherMap"
                },
            }
        },
        "time_zone": 1,
        "name": "Obermatschingen"
    },

}


class Schedules:
    @staticmethod
    def get_weather(location, timestamp, aspect):
        return "weather", location, timestamp, aspect

    @staticmethod
    def get_astronomy(location, timestamp, aspect):
        return "astronomy", location, timestamp, aspect


def merge(map_one, map_two) -> map:
    return {}


def add_schedule(schedule):
    global main_schedules
    main_schedules.append(schedule)


def do_schedules(schedules):
    pass


def mainloop():
    while _mainloop:
        temp = copy.deepcopy(main_schedules)
        do_schedules(main_schedules)


def data_arrival_handler(location, weather, astronomy):
    global database
    database = merge(database, weather)


main_schedules = []
_mainloop: bool = True
