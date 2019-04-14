from datetime import datetime, timedelta
import json
from tabulate import tabulate


PIC = "BASSONS"

def parseFlights(filename):
    with open(filename) as f:
        
        flights = []

        logbook = json.load(f)["flights"]

        for f in logbook:

            flight = {
                    "departureTime": datetime.fromisoformat(f["departureTime"]),
                    "arrivalTime": datetime.fromisoformat(f["arrivalTime"]),
                    "departurePlace": f["departurePlace"],
                    "arrivalPlace": f["arrivalPlace"],
                    "type": f["type"],
                    "registration": f["registration"],
                    "pic": f["pic"],
                    "landings": f["landings"]
            }

            flights.append(flight)

        return flights

def printFlights(flights):
    headers = ["Date", "Dep. Place", "Dep. Time", "Arr Place", "Arr Time", "Type", "Reg.", "Total Time", "PIC Name", "Landings", "PIC", "Double"]
    rows = []

    totalPageTime = timedelta()
    picPageTime = timedelta()
    doublePageTime = timedelta()

    totalTime = timedelta()
    picTime = timedelta()
    doubleTime = timedelta()


    i = 0
    for flight in flights:
        flightTime = flight["arrivalTime"] - flight["departureTime"]
        totalPageTime += flightTime

        row = [
                flight["departureTime"].strftime("%d/%m/%Y"), 
                flight["departurePlace"], 
                flight["departureTime"].strftime("%H:%M"),
                flight["arrivalPlace"],
                flight["arrivalTime"].strftime("%H:%M"),
                flight["type"],
                flight["registration"],
                str(flightTime),
                flight["pic"],
                flight["landings"]
       ]

        if flight["pic"] == PIC:
            picPageTime += flightTime
            row.append(str(flightTime))
            row.append("00:00")
        else:
            doublePageTime += flightTime
            row.append("00:00")
            row.append(str(flightTime))

        rows.append(row)

        if i == 4 or flight == flights[-1]:
            i = 0

            rows.append(["", "", "", "", "", "", "Total PAGE:", str(totalPageTime), "", "", str(picPageTime), str(doublePageTime)])
            rows.append(["", "", "", "", "", "", "Total PREV:", str(totalTime), "", "", str(picTime), str(doubleTime)])
 
            totalTime += totalPageTime
            picTime += picPageTime
            doubleTime += doublePageTime

            rows.append(["", "", "", "", "", "", "Total:", str(totalTime), "", "", str(picTime), str(doubleTime)])
 
            totalPageTime = timedelta()
            picPageTime = timedelta()
            doublePageTime = timedelta()


            for j in range(0,2):
                rows.append([])


    print(tabulate(rows, headers))


flights = parseFlights("logbook.json")
printFlights(flights)


