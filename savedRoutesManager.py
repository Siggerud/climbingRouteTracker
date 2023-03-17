from os import path

class SavedRoutesManager:
    def __init__(self, filename, country, crag):
        self._filename = filename
        self._createFileIfNonExistent()
        self._countryKey = "country_Section"
        self._cragKey = "crag_Section"
        self._country = country
        self._crag = crag
        self._cragStart = 0 # index of first route on crag
        self._cragEnd = 0 # index of last route on crag
        self._countryStart = 0 # index of first entry under country
        self._countryEnd = 0 # index of last entry under country
        self._countryRegistered = self._checkIfCountryRegistered()
        self._cragRegistered = self._checkIfCragRegistered()

    def get_all_lines(self):
        file = open("ascendedRoutes.txt", "r")
        lines = file.readlines()
        file.close()
        print(lines)
        return lines
    def get_if_crag_registered(self):
        return self._cragRegistered

    def get_if_country_registered(self):
        return self._countryRegistered

    def _createFileIfNonExistent(self):
        filename = self._filename
        if not path.isfile(filename):
            file = open(filename, "w+")
            file.close()

    def _addCountry(self):
        file, lines = self._getFileAndLines()
        lines.append(f"{self._countryKey},{self._country}\n")
        self._countryStart = len(lines)  # update countrystart
        file.close()

        self._writeLines(lines)

    def _addCrag(self):
        file, lines = self._getFileAndLines()
        lines.insert(self._countryStart, f"{self._cragKey},{self._crag}\n")
        self._cragStart = self._countryStart + 1
        file.close()

        self._writeLines(lines)

    def deleteAscends(self, routes):
        file, lines = self._getFileAndLines()
        linesToBeRemoved = []
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
        file.close()

        for line in linesToBeRemoved:
            lines.remove(line)
        numberOfDeletes = len(linesToBeRemoved)
        self._updateCragEnd(numberOfDeletes, delete=True)
        if self._cragEnd < self._cragStart: # no more routes registered on crag
            del lines[self._cragStart - 1] # deletes crag title line
            if self._countryEnd == self._countryStart - len(linesToBeRemoved): # no more routes registered on country
                del lines[self._countryStart - 1] # deletes country title line
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

        file, lines = self._getFileAndLines()
        for route in routes:
            routeName = route[0]; routeStyle = route[1]
            lines.insert(self._cragStart, routeName + "," + routeStyle)
        file.close()
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

    def _getFileAndLines(self):
        file = open(self._filename, "r")
        lines = file.readlines()

        return file, lines

    def _checkIfCountryRegistered(self):
        file, lines = self._getFileAndLines()
        countryFound = False
        for index, line in enumerate(lines):
            words = line.strip().split(",")
            if words[0] == self._countryKey and words[1].strip() == self._country:
                self._countryStart = index + 1
                countryFound = True
                break

        file.close()

        return countryFound

    # TODO: identify submethods for method below
    def _checkIfCragRegistered(self):
        if self._countryRegistered == False:
            return False

        file, lines = self._getFileAndLines()

        cragFound = False
        endOfFile = True
        nextCountryFound = False
        for index, line in enumerate(lines[self._countryStart:]):
            words = line.strip().split(",")
            if words[0] == self._cragKey and words[1] == self._crag:
                cragFound = True
                self._cragStart = self._countryStart + index + 1
            elif (words[0] == self._cragKey or words[0] == self._countryKey) and cragFound == True:
                cragEnd = self._countryStart + index - 1
                endOfFile = False
            elif words[0] == self._countryKey: # break if reading on a new country
                nextCountryFound = True
                break

        file.close()

        if nextCountryFound:
            self._countryEnd = self._countryStart + index - 1

        if cragFound == False:
            return False

        if not endOfFile:
            self._cragEnd = cragEnd
        else:
            self._cragEnd = len(lines)

        return True






