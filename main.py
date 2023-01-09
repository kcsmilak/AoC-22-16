
inputFilename = "input.txt"

# name, rate, tunnels[]
#DD @ 2 --> 28
#BB @ 5 --> 25
#JJ @ 9 --> 21
#HH @ 17 -> 13
#DD @ 21 ->  9
#CC @ 24 ->  6

WRONG = [571]

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

def arrayCopy(input):
    output = []
    for v in input: output.append(v)
    return output

def dictCopy(input):
    output = dict()
    for v in input: output[v] = input[v]
    return output
    
def findPath(valves, current, end, trail = [], best = 100):

    # skip paths which we've already visited
    if current in trail:
        return 0, trail

    # end paths which are too long
    if len(current) > best:
        return 0, trail

    # remember where we're at
    trail.append(current)

    # if at the end, we're done!
    if current == end:
        return 1, trail

    round_trail = []
    round_best = best
    # otherwise, try each other path
    for tunnel in valves[current]["tunnels"]:
        success, t = findPath(valves, tunnel, end, arrayCopy(trail), round_best)
        if success and len(t) < round_best:
            round_trail = t
            round_best = len(t)

    if len(round_trail) > 0:
        return 1, round_trail
    else:
        return 0, trail


def run():

    input = processInput(inputFilename)
    #print(input)

    valves = dict()
    for valve in input:
        valves[valve["name"]] = valve
        valve["open"] = False
        valve["examined"] = False

    #print(valves)    

    for name, valve in valves.items():
        if valve["rate"] > 0 :
            print(name, valve["rate"])
            
    #success, trail = findPath(valves, "JJ", "HH", [], 100)
    #print(trail)

    valvesRemaining = list()
    for valve in valves.values():
        if valve["rate"] > 0:
            valvesRemaining.append(valve)
    #print(valvesRemaining)

    print("\t", end="")
    for name, valve in valves.items():
        if valve["rate"] <= 0 and name != "AA": continue
        print(name, end="\t")
    print()
    
    costs = dict()
    targets = list()

    preloadCosts = 1
    if (preloadCosts):
        for line in open("input2.txt"):
            #line = line.strip()
            if len(targets) == 0: 
                line = line.strip()
                targets = line.split("  ")
                #print(targets)
                continue
            current = ""
            for i, cost in enumerate(line.split("  ")):
                if i == 0: 
                    current = cost.strip()
                else:
                    #print("adding", current, targets[i-1].strip(), cost)
                    costs[(current, targets[i-1])] = int(cost.strip())
                    pass
    else:
    
        for sname, svalve in valves.items():
            if svalve["rate"] <= 0 and sname != "AA": continue
            print(sname, end="\t")
            for ename, evalve in valves.items():
                if evalve["rate"] <= 0 and ename != "AA": continue
                success, atrail = findPath(valves, sname, ename, [], 100)
                print(len(atrail)-1, end="\t")
                key = (sname, ename)
                costs[key] = len(atrail)-1
            print()

    
    
    # first, figure cost to travel from any given node to any other


    print("..",flush=True)

    #print(costs)

    current = "AA"
    timeRemaining = 30

    for targetValve in valvesRemaining:
        target = targetValve["name"]
        cost = costs[(current, target)]
        
        benefit =( timeRemaining - cost ) * targetValve["rate"] 
        
        print(target,cost, benefit)

    valveSet = dict()
    for valve in valvesRemaining:
        valveSet[valve["name"]] = -1

    print(valveSet)
        
    # brute force option
    max = 0
    toVisit = list()
    toVisit.append(("AA", 31, valveSet, []))
    while len(toVisit) > 0:
        current, t, valveSet, path = toVisit.pop()
        if t<=0:
            print("at end")
            return
        valveSet[current] = t - 1

        # look at each of the unvisited nodes, decide which to visit first
        for target in valveSet:
            if (valveSet[target] == -1):
                #print(target)
                # append the target and keep looking
                cost = costs[(current, target)]
                toVisit.append((target, t-cost-1, dictCopy(valveSet), path+[target]))
                
        power = 0
        for valve in valveSet:
            power += valveSet[valve]*valves[valve]["rate"]
        if power > max:
            max = power
            print(t, power, valveSet)

def run2():

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