import importlib
import os
import Core.error_handler as eh
import json
from jsonschema import validate
import matplotlib.pyplot as plt
from Plugin.API_constants import UNKNOWN
import GUI.DataVisualisation as data_visualizations

plugin_config_schema = json.loads(open("Plugin/API_config_json_schema.json").read())

files = os.listdir("Plugin/Plugins")


class API:
    def __init__(self, plugin, config_json):
        self.get_database_snippet = None
        self.get_status = lambda: UNKNOWN
        self.is_api = config_json["api"]["has"]
        if self.is_api:
            if config_json["api"]["api_functions"]:
                api_function_path = config_json["api"]["api_functions"]
                self.api_functions = []
                for function in eval("plugin.main." + api_function_path):
                    pass

            if config_json["api"]["get_status"]:
                self.get_status = eval("plugin.main." + config_json["api"]["get_status"])


class Plugin:
    def __init__(self, config_json, folder):
        self.folder = folder
        self.name = config_json["name"]
        self.main_string = config_json["main"]
        import_main = os.path.splitext(self.main_string)[0]
        self.main = importlib.import_module(f"Plugin.Plugins.{folder}.{import_main}")
        if config_json["config"]:
            self.config = eval("self.main." + config_json["config"])
        else:
            self.config = lambda: print(end="")
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
            if "config.json" not in os.listdir(f"Plugin/Plugins/{file}"):
                continue

            plugin_config = json.loads(open(f"Plugin/Plugins/{file}/config.json", "r", encoding="utf-8").read())
            validate(plugin_config, plugin_config_schema)

            name = plugin_config["name"]

            plugin = Plugin(plugin_config, file)

            print(f"[Core] Imported Plugin {plugin.name}")
            plugins.append(plugin)
        except Exception as e:
            eh.error(f"[Core] Couldn't import plugin \"{name}\": {e}.")
    print(f"[Core] {len(plugins)} Plugins loaded.")
    return plugins


def get_apis(plugins):
    apis = []
    for plugin in plugins:
        if plugin.api.is_api:
            apis.append(plugin)
    return apis


def get_matplotlib_figure_weather():
    return data_visualizations.get_matplotlib_figure_weather_new()


print("[CORE] loading plugins")
plugins = load_plugins()
api_plugins = get_apis(plugins)
