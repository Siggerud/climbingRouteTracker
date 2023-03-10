class SavedRoutesManager:
    def __init__(self, filename, country, crag):
        self._filename = filename
        self._country = country
        self._crag = crag
        self._cragStart = 0
        self._cragEnd = 0
        self._countryStart = 0
        self._cragStart = 0
        self._countryRegistered = self._checkIfCountryRegistered()
        self._cragRegistered = self._checkIfCragRegistered()
        self._checkIfCragRegistered()

    def _addCountry(self):
        file = open(self._filename, "a")
        file.writelines(f"\ncountry_Sector:,{self._country}")
        file.close()

    def _addCrag(self):
        file = open(self._filename, "r")
        lines = file.readlines()
        lines.insert(self._countryStart, f"crag_Section:,{self._crag}\n")
        self._cragStart = self._countryStart + 1
        file.close()

        self._writeLines(lines)

    # TODO: make event when submitting, either close form or popup window
    def registerAscends(self, routes):
        if not self._countryRegistered:
            self._addCountry()
            self._addCrag()
        elif not self._cragRegistered:
            self._addCrag()

        file = open(self._filename, "r")
        lines = file.readlines()
        for route in routes:
            name = route[0]; style = route[1]
            lines.insert(self._cragStart, name + "," + style + "\n")
        file.close()

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
        lines = file.readlines()[self._cragStart:self._cragEnd]
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
        for index, line in enumerate(lines[self._countryStart:]):
            words = line.strip().split(",")
            if words[0] == "crag_Section:" and words[1] == self._crag:
                cragFound = True
                cragStart = self._countryStart + index + 1
            elif (words[0] == "crag_Section:" or words[0] == "country_Section:") and cragFound == True:
                self._cragEnd = cragStart + index
                endOfFile = False
                break
            elif words[0] == "country_Section:": # break if reading on a new country
                break

        file.close()

        if cragFound == False:
            return False

        self._cragStart = cragStart
        self._cragRegistered = True
        if endOfFile:
            self._cragEnd = len(lines)






