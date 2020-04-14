import importlib
import os
import Core.error_handler as eh

files = os.listdir("API/APIs")

apis = []

for file in files:
    try:
        if not "Main.py" in os.listdir(f"API/APIs/{file}"):
            continue
        api = importlib.import_module(f"API.APIs.{file}.Main")
        print(f"[Core] Name: {api.NAME}")
        garbage = api.CONFIG = api.get_status
        apis.append(api)
    except Exception as e:
        eh.error(f"[Core] File {file} in API/APIs is not a valid module, {e}.")
print(f"[Core] {len(apis)} APIs detected.")
