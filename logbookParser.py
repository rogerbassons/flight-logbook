from datetime import datetime, timedelta
import json
from tabulate import tabulate
import sys
import argparse

FILENAME="logbook.json"
PIC = "BASSONS"
ROWS_PAGE = 14

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

    lastYearTime = timedelta()
    dateLastYear = None
    if (len(flights) > 0):
        dateLastYear = flights[-1]["departureTime"] - timedelta(days=(365.24))

    pageLandings = 0
    totalPageTime = timedelta()
    picPageTime = timedelta()
    doublePageTime = timedelta()

    landings = 0
    totalTime = timedelta()
    picTime = timedelta()
    doubleTime = timedelta()


    i = 0
    for flight in flights:
        flightTime = flight["arrivalTime"] - flight["departureTime"]
        totalPageTime += flightTime
        pageLandings += flight["landings"]

        if (dateLastYear != None and dateLastYear < flight["departureTime"]):
            lastYearTime += flightTime

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

        if i == ROWS_PAGE - 1 or flight == flights[-1]:
            i = 0

            rows += [""]

            rows.append(["", "", "", "", "", "", "Total PAGE:", str(totalPageTime), "", str(pageLandings), str(picPageTime), str(doublePageTime)])
            rows.append(["", "", "", "", "", "", "Total PREV:", str(totalTime), "", str(landings), str(picTime), str(doubleTime)])
 
            landings += pageLandings
            totalTime += totalPageTime
            picTime += picPageTime
            doubleTime += doublePageTime

            rows.append(["", "", "", "", "", "", "Total:", str(totalTime), "", str(landings), str(picTime), str(doubleTime)])
 
            pageLandings = 0
            totalPageTime = timedelta()
            picPageTime = timedelta()
            doublePageTime = timedelta()

            print(tabulate(rows, headers, tablefmt="fancy"))
            print("")
            rows = []
        else:
            i += 1

    
    print("Last year total time: " + str(lastYearTime))



def parseArgs():
    parser = argparse.ArgumentParser(description="Flight logbook")
    parser.add_argument("--from", help="departure airport", required=True)
    parser.add_argument("--arr", help="arrival airport")
    parser.add_argument("--atd", help="actual time of departure", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ate", help="actual time en route")
    group.add_argument("--ata", help="actual time of arrival")
    parser.add_argument("--type", help="aircraft type", required=True)
    parser.add_argument("--reg", help="aircraft registration", required=True)
    parser.add_argument("--pic", help="PIC", default=PIC)
    parser.add_argument("--land", help="number of landings", type=int, default=1)
    return parser.parse_args()

def parseDateTimes(departureTime, arrivalTime, timeEnroute):
    atd = datetime.strptime(departureTime, "%Y-%m-%dT%H:%M")
    ata = None 

    if (arrivalTime == None):
        ate = timeEnroute.split(':')
        hours = 0
        minutes = 0

        if (len(ate) > 1):
            hours, minutes= map(int, ate)
        else:
            minutes = int(ate[0])

        if (minutes >= 60):
            raise ValueError("minutes too big")
        ata = atd + timedelta(hours=hours, minutes=minutes)
    else:
        ata = datetime.strptime(arrivalTime, "%Y-%m-%dT%H:%M")

    return atd, ata


if (len(sys.argv) > 1):
    
    args = parseArgs()

    atd, ata = parseDateTimes(args.atd, args.ata, args.ate)

    departure = getattr(args, "from")
    arr = departure
    if (args.arr != None):
        arr = args.arr
    
    flight = {
            "departurePlace": getattr(args, "from"),
            "departureTime": atd.isoformat(),
	    "arrivalPlace": arr,
	    "arrivalTime": ata.isoformat(),
	    "type": args.type,
	    "registration": args.reg,
	    "pic": args.pic,
	    "landings": args.land
    }

    logbook = None
    with open(FILENAME, "r") as jsonFile:
        
        logbook = json.load(jsonFile)

        logbook["flights"] += [flight]

    with open(FILENAME, "w") as jsonFile:
        if (logbook):
            json.dump(logbook, jsonFile, indent=4)


else:
    flights = parseFlights(FILENAME)
    printFlights(flights)


