import importlib
import os
import Core.error_handler as eh

files = os.listdir("API/APIs")

apis = []

for file in files:
    try:
        api = importlib.import_module(f"API.APIs.{file[:-3]}")
        apis.append(api)
    except Exception as e:
        print(f"[Core] File {file} in API/APIs is not a valid module, {e}.")

print(f"[Core] {len(apis)} APIs detected.")
