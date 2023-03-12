class SavedRoutesManager:
    def __init__(self, filename, country, crag):
        self._filename = filename
        self._country = country
        self._crag = crag
        self._cragStart = 0 # index of first route on crag
        self._cragEnd = 0 # index of last route on crag
        self._countryStart = 0
        self._countryEnd = 0
        self._countryRegistered = self._checkIfCountryRegistered()
        self._cragRegistered = self._checkIfCragRegistered()

    def _addCountry(self):
        file = open(self._filename, "r")
        lines = file.readlines()
        lines.append(f"country_Section:,{self._country}\n")
        self._countryStart = len(lines)  # update countrystart
        file.close()

        self._writeLines(lines)

    #TODO: find out why crag is not being added
    def _addCrag(self):
        file = open(self._filename, "r")
        lines = file.readlines()
        lines.insert(self._countryStart, f"crag_Section:,{self._crag}\n")
        self._cragStart = self._countryStart + 1
        file.close()
        print(lines)

        self._writeLines(lines)

    def deleteAscends(self, routes):
        print(routes)
        file = open(self._filename, "r")
        linesToBeRemoved = []
        lines = file.readlines()
        for index, line in enumerate(lines):
            if index < self._cragStart:
                continue
            elif index > self._cragEnd:
                break
            recordedRoute = line.split(",")
            for route in routes:
                if recordedRoute == route:
                    linesToBeRemoved.append(line)
                    routes.remove(route)
        print(len(linesToBeRemoved))
        print(self._cragStart, self._cragEnd)
        file.close()

        for line in linesToBeRemoved:
            lines.remove(line)
        print(lines)
        numberOfDeletes = len(linesToBeRemoved)
        self._updateCragEnd(numberOfDeletes, delete=True)
        if self._cragEnd < self._cragStart: # no more routes registered on crag
            del lines[self._cragStart - 1] # deletes crag title line
            if self._countryEnd == self._countryStart - len(linesToBeRemoved): # no more routes registered on country
                del lines[self._countryStart - 1] # deletes country title line
        print(lines)
        self._writeLines(lines)

    def _updateCragEnd(self, numberOfRoutes, delete=False):
        if delete:
            self._cragEnd -= numberOfRoutes
        else:
            if not self._cragRegistered:
                self._cragEnd = self._cragStart + numberOfRoutes - 1
            else:
                self._cragEnd += numberOfRoutes

    def registerAscends(self, routes):
        if not self._countryRegistered:
            self._addCountry()
            self._addCrag()
        elif not self._cragRegistered:
            self._addCrag()

        file = open(self._filename, "r")
        lines = file.readlines()
        print(lines)
        for route in routes:
            routeName = route[0]; routeStyle = route[1]
            lines.insert(self._cragStart, routeName + "," + routeStyle)
        file.close()
        print(lines)
        numberOfRegistrations = len(routes)
        self._updateCragEnd(numberOfRegistrations)

        self._writeLines(lines)

    def _writeLines(self, lines):
        file = open(self._filename, "w")
        for line in lines:
            file.writelines(line)
        file.close()

    def checkIfRouteAscended(self, routeName, style):
        if not self._cragRegistered:
            return 0

        file = open(self._filename, "r")
        lines = file.readlines()[self._cragStart:self._cragEnd + 1]
        routeFound = False
        for line in lines:
            words = line.strip().split(",")
            if words[0] == routeName and words[1] == style:
                routeFound = True

        if routeFound:
            return 1
        return 0

    def _checkIfCountryRegistered(self):
        file = open(self._filename, "r")
        lines = file.readlines()
        countryFound = False
        for index, line in enumerate(lines):
            words = line.strip().split(",")
            if words[0] == "country_Section:" and words[1].strip() == self._country:
                self._countryStart = index + 1
                countryFound = True
                break

        file.close()

        return countryFound

    # TODO: identify submethods for method below
    def _checkIfCragRegistered(self):
        if self._countryRegistered == False:
            return False

        file = open(self._filename, "r")
        lines = file.readlines()

        cragFound = False
        endOfFile = True
        nextCountryFound = False
        for index, line in enumerate(lines[self._countryStart:]):
            words = line.strip().split(",")
            if words[0] == "crag_Section:" and words[1] == self._crag:
                cragFound = True
                cragStart = self._countryStart + index + 1
            elif (words[0] == "crag_Section:" or words[0] == "country_Section:") and cragFound == True:
                cragEnd = self._countryStart + index - 1
                endOfFile = False
            elif words[0] == "country_Section:": # break if reading on a new country
                nextCountryFound = True
                break

        file.close()

        if nextCountryFound:
            self._countryEnd = self._countryStart + index - 1

        if cragFound == False:
            return False

        self._cragStart = cragStart
        if not endOfFile:
            self._cragEnd = cragEnd
        else:
            self._cragEnd = len(lines)

        return True






