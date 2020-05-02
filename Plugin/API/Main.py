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
                (12864372876, 12864399934): {
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
                    "weather_name": "good"
                },
            }
        },
        "time_zone": 1,
        "name": "Unknown"
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


def do_schedule(schedules):
    pass


def mainloop():
    while _mainloop:
        temp = copy.deepcopy(main_schedules)
        do_schedule(main_schedules)


def data_arrival_handler(location, weather, astronomy):
    global database
    database = merge(database, weather)


main_schedules = []
_mainloop: bool = True
