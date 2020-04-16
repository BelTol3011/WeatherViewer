import importlib
import os
import Core.error_handler as eh

files = os.listdir("API/APIs")

apis = []


def dms_to_decimal(degrees, min, sec):
    return degrees + (min / 60) + (sec / 3600)


def decimal_to_dms(decimal):
    degrees = int(decimal)
    temp = (decimal - degrees) * 60
    minutes = int(temp)
    seconds = (temp - minutes) * 60
    return degrees, minutes, seconds


for file in files:
    try:
        if not "config.dat" in os.listdir(f"API/APIs/{file}"):
            continue
        api = importlib.import_module(f"API.APIs.{file}.Main")
        print(f"[Core] Imported API {api.NAME}")
        apis.append(api)
    except Exception as e:
        eh.error(f"[Core] File {file} in API/APIs is not a valid module, {e}.")
print(f"[Core] {len(apis)} APIs detected.")

database = {
    # Ort
    "Leipzig": {
        "data": {
            # Tag
            "2020-4-14": {
                # Zeit
                12864372876: {
                    "temperature": {
                        "real": 12,
                        "felt": 13
                    },
                    "wind": {
                        "direction": "NW",
                        "degrees": 310,
                        "speed": 12
                    },
                    "clouds": {
                        "condition": {
                            "WeatherAPI": "Mäßig bewölkt",
                            "OpenWeatherMap": "Mäßig bewölkt"
                        }
                    },
                    "air": {
                        "view_distance": 10000,
                        "pressure": 1000,
                        "humidity": 39
                    }
                },
                1286437286: {
                    "temperature": {
                        "real": 12,
                        "felt": 13
                    },
                    "wind": {
                        "direction": "NW",
                        "degrees": 310,
                        "speed": 12
                    },
                    "clouds": {
                        "condition": {
                            "WeatherAPI": "Mäßig bewölkt",
                            "OpenWeatherMap": "Mäßig bewölkt"
                        }
                    },
                    "air": {
                        "view_distance": 10000,
                        "pressure": 1000,
                        "humidity": 39
                    }
                },
                "astronomy": {
                    "sunset": 283748323,
                    "sunrise": 897634534,
                    "moonset": 8234432278,
                    "moonrise": 237487823,
                    "moon_type": {
                        "WeatherAPI": "Quarter",
                        "OpenWeatherMap": "Quarter"
                    }
                }
            },

        },
        "longitude": 12.3,
        "latitude": 23.2,
        "time_zone": "+1"
    }
}


def get_temperature_for_day(day):
    pass
