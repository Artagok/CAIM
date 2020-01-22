#!/usr/bin/python

from collections import namedtuple
import time
import sys

Colors = {
    'end': '\033[0m',
    'bold': '\033[1m',
    'red': '\033[91m',
    'yell': '\033[93m',
    'blue': '\033[94m',
    'green': '\033[92m',
}


class Edge:
    def __init__ (self, origin=None):
        self.origin = origin
        self.weight = 1.0

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)
        
    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden        # IATA 
        self.name = name        # City, Country
        self.routes = []        # Edges() of airports that have a route to this airport
        self.routeHash = dict() # {IATA: index in routes}
        self.outweight = 0.0    

    # We have an origin airport that points to this(self) airport
    def addEdge(self, origin):
        # We already have a route: orgin -> self
        if origin in self.routeHash:
            i = self.routeHash[origin]
            (self.routes[i]).weight += 1.0
        # We have a new route: orgin -> self
        else:
            edge = Edge(origin)
            edge.index = airportHash[origin].index
            i = len(self.routes)
            self.routes.append(edge)
            self.routeHash[origin] = i


    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)

# ========= Structures ========= #
edgeList = []           # list of Edge
edgeHash = dict()       # hash of edge to ease the match

airportList = []        # list of Airport
airportHash = dict()    # {IATA: Airport}

isolated = 0            # Number of unconnected Airports
PageRank = []           # PageRank vector
# ============================== #

def getAirport(a):
    if a in airportHash:
        return airportHash[a]
    else:
        raise Exception("{0} appears in routes.txt but not in airports.txt".format(a))

def readAirports(fd):
    print("\nReading Airport file from {1}{0}{2}".format(fd,Colors['blue'],Colors['end']))
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
            a.index=cont
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print("There were {1}{2}{0}{3} Airports with IATA code".format(cont,Colors['bold'],Colors['green'],Colors['end']))


def readRoutes(fd):
    print("Reading Routes file from {1}{0}{2}".format(fd,Colors['blue'],Colors['end']))
    # airline code | OP airline code
    # CODE ORIGIN | OP CODE ORIGIN
    # CODE DESTIN | OP CODE DESTIN
    # We are interested in indexes 2 & 4 that are IATA
    routesTxt = open(fd, "r");
    cont = 0
    for line in routesTxt.readlines():
        try:
            temp = line.split(',')
            if len(temp[2]) != 3: raise Exception("{0} is not IATA".format(temp[2]))
            if len(temp[4]) != 3: raise Exception("{0} is not IATA".format(temp[4]))

            iataOrigin = temp[2]
            iataDestin = temp[4]
            airportOrigin = getAirport(iataOrigin)
            airportDestin = getAirport(iataDestin)
            airportDestin.addEdge(iataOrigin)
            airportOrigin.outweight += 1.0
        except Exception as inst:
            pass
        else:
            cont += 1
    routesTxt.close()
    print("There were {1}{2}{0}{3} routes between IATA airports".format(cont,Colors['bold'],Colors['green'],Colors['end']))


def computePageRanks():

    n = len(airportList)            # Number of Vertices(Airports)
    P = [1.0/n for i in range(0,n)] # [1/n, 1/n, 1/n ...]
    L = 0.85                        # Damping factor (0.8 <= L <= 0.9)
    iterations = 0                  # Number of PageRank iterations 
    auxIsolated = 1.0/n             # Isolated factor
    stopCondition = False           # Algorithm Stopping Condition. The lower the threshold the harder it is to stop
    threshold = 1.0e-10             # Threshold factor, PR stops when for all P we have: abs(P[i] - P[i-1]) < threshold
    rounding = 4                    # Number of decimals to round floats to
    print('Stopping threshold = {0}{2}{1}\nRounding floats to the {0}{3}{1} decimal'.format(Colors['bold'],Colors['end'],threshold,rounding))
    print("~~~ {0}Starting{1} PageRank Computation ~~~".format(Colors['green'], Colors['end']))

    while not stopCondition:
        Q = [0.0 for i in range(0,n)]
        
        for i in range(0,n):
            airport = airportList[i]
            suma = 0

            for edge in airport.routes:
                out = airportHash[edge.origin].outweight
                suma += P[edge.index] * edge.weight / out 

            Q[i] = L * suma + (1.0-L)/n + auxIsolated * L/float(n)*isolated
        
        auxIsolated = (1.0 - L)/n + auxIsolated*L/float(n)*isolated
        stopCondition = all(list(map(lambda x: x < threshold,[abs(a-b) for a,b in zip(P,Q)])))
        
        print('i={2}{0}{3}\tsum(P)={2}{1}{3}'.format(iterations,round(sum(P),rounding),Colors['yell'],Colors['end']))
        iterations += 1
        P = Q

    print("~~~ {0}Ending{1} PageRank Computation ~~~\n".format(Colors['red'], Colors['end']))
    global PageRank
    PageRank = P
    return iterations


def outputPageRanks():
    # PageRank is sorted the same way as airportList
    # Meaning PageRank[i] is the value for the airport in airportList[i]

    rounding = 10
    result = sorted(zip(PageRank, airportList), key = lambda x: x[0], reverse=True)
    
    for pr, a in result:
        print('{3}{0}{5}\t{4}{1}{5} {2}'.format(round(pr,rounding),a.code,a.name,Colors['yell'],Colors['green'],Colors['end']))
    print()

def main(argv=None):
    
    readAirports("airports.txt")
    readRoutes("routes.txt")

    global isolated
    isolated = len([x for x in airportList if x.outweight == 0.0])

    print('There were {3}{0}{1}{2} isolated airports\n'.format(Colors['red'],isolated,Colors['end'],Colors['bold']))

    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()

    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2-time1, 'seconds')
    print('Sum(PageRank) = {0}'.format(round(sum(PageRank),4)))


if __name__ == "__main__":
    sys.exit(main())
