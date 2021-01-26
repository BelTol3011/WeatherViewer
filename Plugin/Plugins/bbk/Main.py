import requests
import json
import time

# https://warnung.bund.de/bbk.mowas/gefahrendurchsagen.json

print("[BBK] Getting warning data from the BBK")
t1 = time.time()
data = requests.get("https://warnung.bund.de/bbk.mowas/gefahrendurchsagen.json")
print("[BBK] size:", len(data.text), "characters")
data = json.loads(data.text)
t2 = time.time()
print(f"[BBK] ... finished (took {round(t2 - t1, 1)} seconds)")

for element in data:
    for parameter in element:
        print(parameter, ":", element[parameter])
