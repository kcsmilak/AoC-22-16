
inputFilename = "example.txt"

# name, rate, tunnels[]

def processInput(inputFilename):
    input = []
    inputStream = open(inputFilename, "r")

    for line in inputStream:
        line = line.strip()

        row = {}

        row["name"] = line.split(" ")[1]
        row["rate"] = int(line.split("=")[1].split(";")[0])
        potentialValves = line.split("valv")[1].split(" ")
        valves = []
        for potentialValve in potentialValves:
            if (potentialValve == "es" or potentialValve == "e"): continue
            potentialValve = potentialValve.strip(",")
            valves.append(potentialValve)
        
        row["tunnels"] = valves


        
        input.append(row)

    inputStream.close()
    return input




def run():

    input = processInput(inputFilename)
    #print(input)

    valves = {}
    for valve in input:
        valves[valve["name"]] = valve
        valve["open"] = False
        valve["examined"] = False

    #print(valves)

    examinedValves = {}
    openValves = {}

    valve = valves[input[0]["name"]]
    pressureRelease = 0
    
    waiting = False
    for minute in range(1,20,1):
        print("== Minute {0} == {1}".format(minute, valve["name"]))


        pressureRelease = 0
        for key in openValves:
            pressureRelease += openValves[key]
        print("Open valves {0} for total rate {1}".format(openValves, pressureRelease))

        if waiting:
            waiting = False
        else:

            examinedValves[valve["name"]] = True
            
            # if current valve not open and not stuck, then open
            if not valve["open"] and valve["rate"] > 0:
                #waiting = True
                valve["open"] = True
                openValves[valve["name"]] = valve["rate"]
                print("You open valve {0} ({1}).".format(valve["name"],valve["rate"]))
            
            # else move to unexamined tunnel
            else:            
                #print(valve["tunnels"])
                for tunnel in valve["tunnels"]:
                    if not tunnel in examinedValves:
                        valve = valves[valve["tunnels"][0]]
                        break
                print("You move to valve {0}.".format(valve["name"]))

        print("")

if __name__ == '__main__':
  run()