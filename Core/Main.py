import importlib
import os
import Core.error_handler as eh
import json
from jsonschema import validate
import matplotlib.pyplot as plt
import numpy as np
import API.Main as ApiMain

plugin_config_schema = json.loads(open("API/API_config_json_schema.json").read())

files = os.listdir("API/APIs")


class API:
    def __init__(self, plugin, config_json):
        self.get_database_snippet = None
        self.get_status = None
        self.is_api = config_json["api"]["has"]
        if self.is_api:
            if config_json["api"]["get_database_snippet"]:
                self.get_database_snippet = eval("self.main." + config_json["api"]["get_database_snippet"])
            if config_json["api"]["get_status"]:
                self.get_status = eval("plugin.main." + config_json["api"]["get_status"])


class Plugin:
    def __init__(self, config_json, folder):
        self.folder = folder
        self.name = config_json["name"]
        self.main_string = config_json["main"]
        import_main = os.path.splitext(self.main_string)[0]
        self.main = importlib.import_module(f"API.APIs.{folder}.{import_main}")
        self.config = eval("self.main." + config_json["config"])
        if config_json["search_city_list"]:
            self.search_city_list = eval("self.main." + config_json["search_city_list"])
            self.format = eval("self.main." + config_json["format"])
        else:
            self.search_city_list = None

        self.api = API(self, config_json)


def dms_to_decimal(degrees, min, sec):
    return degrees + (min / 60) + (sec / 3600)


def decimal_to_dms(decimal):
    degrees = int(decimal)
    temp = (decimal - degrees) * 60
    minutes = int(temp)
    seconds = (temp - minutes) * 60
    return degrees, minutes, seconds


def load_plugins():
    plugins = []
    for file in files:
        name = "unknown"
        try:
            if "config.json" not in os.listdir(f"API/APIs/{file}"):
                continue

            plugin_config = json.loads(open(f"API/APIs/{file}/config.json").read())
            validate(plugin_config, plugin_config_schema)

            name = plugin_config["name"]

            plugin = Plugin(plugin_config, file)

            print(f"[Core] Imported API {plugin.name}")
            plugins.append(plugin)
        except Exception as e:
            eh.error(f"[Core] Couldn't import plugin \"{name}\": {e}.")
    print(f"[Core] {len(plugins)} Plugins detected.")
    return plugins


def get_apis(plugins):
    apis = []
    for plugin in plugins:
        if plugin.api.is_api:
            apis.append(plugin)
    return apis


def get_matplotlib_figure_weather():
    # alter Aufruf

    return plt.Figure()


plugins = load_plugins()
api_plugins = get_apis(plugins)


database = {
    # Ort
    (12.3, 23.2): {
        "data": {
            "astronomy": {
                "2020-04-14": {"sunset": 283748323,
                               "sunrise": 897634534,
                               "moonset": 8234432278,
                               "moonrise": 237487823,
                               "moon_type": {
                                   "WeatherAPI": "Quarter",
                                   "OpenWeatherMap": "Quarter"
                               }
                               },

            },
            "weather": {
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
                            "OpenWeatherMap": "Mittel bewölkt"
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
                        "real": -102,
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
            }
        },
        "time_zone": 1
    },
    (-2.3337, 13.6): {
        "data": {
            "astronomy": {
                "2020-04-14": {"sunset": 283748323,
                               "sunrise": 897634534,
                               "moonset": 8234432278,
                               "moonrise": 237487823,
                               "moon_type": {
                                   "WeatherAPI": "Quarter",
                                   "OpenWeatherMap": "Quarter"
                               }
                               },

            },
            "weather": {
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
                            "OpenWeatherMap": "Mittel bewölkt"
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
            }
        },
        "time_zone": 1
    },
    (-7.5723, -24.2226): {
        "data": {
            "astronomy": {
                "2020-04-14": {"sunset": 283748323,
                               "sunrise": 897634534,
                               "moonset": 8234432278,
                               "moonrise": 237487823,
                               "moon_type": {
                                   "WeatherAPI": "Quarter",
                                   "OpenWeatherMap": "Quarter"
                               }
                               },

            },
            "weather": {
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
                            "OpenWeatherMap": "Mittel bewölkt"
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
            }
        },
        "time_zone": 1
    },
}

# for key in database[(12.3, 23.2)]["data"]["weather"]:
#     print(key, database[(12.3, 23.2)]["data"]["weather"][key]["temperature"]["real"])
