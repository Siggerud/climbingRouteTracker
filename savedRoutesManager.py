from os import path

class SavedRoutesManager:
    # manages ascended routes
    def __init__(self, filename, country, crag):
        self._filename = filename
        self._create_file_if_nonexistent()
        self._countryKey = "country_Section"
        self._cragKey = "crag_Section"
        self._country = country
        self._crag = crag
        self._cragStart = 0 # index of first route on crag
        self._cragEnd = 0 # index of last route on crag
        self._countryStart = 0 # index of first entry under country
        self._countryEnd = 0 # index of last entry under country
        self._countryRegistered = self._check_if_country_registered()
        self._cragRegistered = self._check_if_crag_registered()

    # returns the _cragEnd. Mainly for testing purposes
    def get_crag_end(self):
        return self._cragEnd

    # returns all lines currently in txt file. Mainly for testing purposes
    def get_all_lines(self):
        file = open(self._filename, "r")
        lines = file.readlines()
        file.close()

        return lines

    # returns _cragRegistered. Mainly for testing purposes
    def get_if_crag_registered(self):
        return self._cragRegistered

    # returns _countryRegistered. Mainly for testing purposes
    def get_if_country_registered(self):
        return self._countryRegistered

    # creates a file for keeping track of ascended routes if file doesn't exist
    def _create_file_if_nonexistent(self):
        filename = self._filename
        if not path.isfile(filename):
            file = open(filename, "w+")
            file.close()

    # adds country to txt file
    def _add_country(self):
        file, lines = self._get_file_and_lines()
        lines.append(f"{self._countryKey},{self._country}\n")
        self._countryStart = len(lines)  # update countrystart
        file.close()

        self._write_lines(lines)

    # adds crag to txt file
    def _add_crag(self):
        file, lines = self._get_file_and_lines()
        # insert at country crag belongs to
        lines.insert(self._countryStart, f"{self._cragKey},{self._crag}\n")
        self._cragStart = self._countryStart + 1
        file.close()

        self._write_lines(lines)

    # deletes previous ascents from txt file
    def delete_ascends(self, routes):
        file, lines = self._get_file_and_lines()
        linesToBeRemoved = []
        # find which lines are to be deleted
        for index, line in enumerate(lines):
            # don't search outside of crag scope
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

        # delete lines
        for line in linesToBeRemoved:
            lines.remove(line)
        numberOfDeletes = len(linesToBeRemoved)
        self._update_crag_end(numberOfDeletes, delete=True)
        if self._cragEnd < self._cragStart: # no more routes registered on crag
            del lines[self._cragStart - 1] # deletes crag title line
            if self._countryStart == self._countryEnd - numberOfDeletes: # no more routes registered on country
                del lines[self._countryStart - 1] # deletes country title line
        self._write_lines(lines)

    # updates _cragEnd
    def _update_crag_end(self, numberOfRoutes, delete=False):
        # subtract if routes have been deleted
        if delete:
            self._cragEnd -= numberOfRoutes
        else:
            if not self._cragRegistered:
                self._cragEnd = self._cragStart + numberOfRoutes - 1
            else:
                self._cragEnd += numberOfRoutes

    # registers new ascends in txt file
    def register_ascends(self, routes):
        # adds country and crag if not registered before
        if not self._countryRegistered:
            self._add_country()
            self._add_crag()
        elif not self._cragRegistered:
            self._add_crag()

        file, lines = self._get_file_and_lines()
        for route in routes:
            routeName = route[0]; routeStyle = route[1]
            # insert routes at crag start
            lines.insert(self._cragStart, routeName + "," + routeStyle)
        file.close()
        numberOfRegistrations = len(routes)
        self._update_crag_end(numberOfRegistrations) # update cragEnd

        self._write_lines(lines)

    # write lines given as argument to txt file
    def _write_lines(self, lines):
        file = open(self._filename, "w")
        for line in lines:
            file.writelines(line)
        file.close()

    # checks if route is already registered
    def check_if_route_ascended(self, routeName, style):
        # crag must be registered for route to be registered
        if not self._cragRegistered:
            return False

        file = open(self._filename, "r")
        lines = file.readlines()[self._cragStart:self._cragEnd + 1]
        routeFound = False
        # search for route in txt file
        for line in lines:
            words = line.strip().split(",")
            if words[0] == routeName and words[1] == style:
                routeFound = True

        if routeFound:
            return True
        return False

    # returns file and lines given by _filename
    def _get_file_and_lines(self):
        file = open(self._filename, "r")
        lines = file.readlines()

        return file, lines

    # checks if country is registered
    def _check_if_country_registered(self):
        file, lines = self._get_file_and_lines()
        countryFound = False
        nextCountryFound = False
        for index, line in enumerate(lines):
            words = line.strip().split(",")
            if words[0] == self._countryKey and words[1].strip() == self._country:
                self._countryStart = index + 1 # set countryStart if country found
                countryFound = True
            elif words[0] == self._countryKey and countryFound:
                nextCountryFound = True
                self._countryEnd = index - 1 # set countryEnd if a new country is found
                break

        # if country is the last country in list, set countryEnd to be end of file
        if countryFound and not nextCountryFound:
            self._countryEnd = len(lines) - 1

        file.close()

        return countryFound

    def _check_if_crag_registered(self):
        # country must be registered for crag to be registered
        if self._countryRegistered == False:
            return False

        file, lines = self._get_file_and_lines()

        cragFound = False
        nextCragFound = False
        # search within country scope
        for index, line in enumerate(lines[self._countryStart:self._countryEnd + 1]):
            words = line.strip().split(",")
            if words[0] == self._cragKey and words[1] == self._crag:
                cragFound = True
                self._cragStart = self._countryStart + index + 1 # set _cragStart
            elif words[0] == self._cragKey and cragFound == True:
                # if next crag is found, set _cragEnd
                self._cragEnd = self._countryStart + index - 1
                nextCragFound = True
                break

        file.close()

        if cragFound == False:
            return False

        # if next crag is not found, _cragEnd is set as _countryEnd
        if not nextCragFound:
            self._cragEnd = self._countryEnd

        return True






