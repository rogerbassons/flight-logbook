from pyexcel_odsr import get_data
from datetime import datetime
import json

logbook = get_data("logbook.ods")["Sheet2"]


flights = []

i=1

for f in logbook:
    print(i)
    i = i + 1

    departureTime = datetime(year=f[0].year, month=f[0].month, day=f[0].day, hour=f[2].hour, minute=f[2].minute)
    arrivalTime = datetime(year=f[0].year, month=f[0].month, day=f[0].day, hour=f[4].hour, minute=f[4].minute)

    flight = {
            "departureTime": departureTime.isoformat(),
            "arrivalTime": arrivalTime.isoformat(),
            "departurePlace": f[1],
            "arrivalPlace": f[3],
            "type": f[5],
            "registration": f[6],
            "pic": f[10],
            "landings": f[11]
    }

    flights.append(flight)

data = { "flights": flights }
with open("logbook.json", "w") as jsonFile:
    json.dump(data, jsonFile, indent=4)
print("Wrote " + str(i) + " flights.")


