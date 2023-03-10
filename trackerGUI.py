from tkinter import Tk, ttk, StringVar, Checkbutton, Listbox, Variable, Frame, Label, \
    Toplevel, Button, IntVar
from scraper import CragScraper
from scrapeCleaner import ScrapeCleaner
from savedRoutesManager import SavedRoutesManager

# TODO: make sure the scraping only gets executed at the start of the program

class trackerGUI:
    def __init__(self, master):
        self._master = master
        self._master.geometry("300x400")
        self._master.title("Climbing routes tracker")

        self._cragInfo = []
        self._ascendedRoutes = []
        self._scraper = CragScraper()
        self._cleaner = ScrapeCleaner()

        self._continentVar = StringVar()
        self._continent = ttk.Combobox(self._master, textvariable=self._continentVar, width=10)
        self._continent.place(x=10, y=10)
        self._setContinent()

        self._continent.bind("<<ComboboxSelected>>", self._updateCountries)

        self._countryVar = StringVar()
        self._country = ttk.Combobox(self._master, textvariable=self._countryVar, width=10)
        self._country.place(x=10, y=40)
        self._setCountries()

        self._country.bind("<<ComboboxSelected>>", self._updateCrags)

        self._styleSportVar = StringVar()
        self._styleSport = Checkbutton(self._master, text="Sport", variable=self._styleSportVar,
                                       onvalue="sport", offvalue="", command=self._getResults)
        self._styleSport.place(x=5, y=70)

        self._styleTradVar = StringVar()
        self._styleTrad = Checkbutton(self._master, text="Trad", variable=self._styleTradVar,
                                       onvalue="trad", offvalue="", command=self._getResults)
        self._styleTrad.place(x=65, y=70)

        self._styleBoulderVar = StringVar()
        self._styleBoulder = Checkbutton(self._master, text="Boulder", variable=self._styleBoulderVar,
                                      onvalue="boulder", offvalue="", command=self._getResults)
        self._styleBoulder.place(x=125, y=70)

        self._styleDwsVar = StringVar()
        self._styleDws = Checkbutton(self._master, text="DWS", variable=self._styleDwsVar,
                                      onvalue="DWS", offvalue="", command=self._getResults)
        self._styleDws.place(x=5, y=95)

        self._resultVar = Variable()
        self._resultList = Listbox(self._master, listvariable=self._resultVar, height=15)
        self._resultList.place(x=5, y=125)

        self._scrapeResults()
        self._getResults()

        self._resultList.bind('<<ListboxSelect>>', self._showCragGradeInfo)

        self._cragGradeInfoFrame = Frame(self._master)
        self._cragGradeInfoFrame.place(x=150, y=125)

    def _showCragGradeInfo(self, event):
        if self._resultList.curselection() == ():
            return

        for widget in self._cragGradeInfoFrame.winfo_children():
            widget.destroy()

        cragGradeLabel = Label(self._cragGradeInfoFrame, text="Grade")
        cragGradeLabel.grid(row=0, column=0)

        cragNumberLabel = Label(self._cragGradeInfoFrame, text="Number")
        cragNumberLabel.grid(row=0, column=1)

        gradeSummary = self._getGradeSummary()
        rowCount = 1
        for grade, number in gradeSummary.items():
            gradeLabel = Label(self._cragGradeInfoFrame, text=grade)
            gradeLabel.grid(row=rowCount, column=0, sticky="w")

            numberLabel = Label(self._cragGradeInfoFrame, text=number)
            numberLabel.grid(row=rowCount, column=1, sticky="w")

            rowCount += 1

        markButton = Button(self._cragGradeInfoFrame, text="Mark ascents", bg="springgreen", command=self._makePopup)
        markButton.grid(row=rowCount, column=0, sticky="w", columnspan=2)

    #TODO: lag scrollbar
    def _makePopup(self):
        self._markAscendsWindow = Toplevel(self._master)
        self._markAscendsWindow.geometry("300x500")
        self._markAscendsWindow.title("Mark ascents")

        url = self._getCragUrl()
        cragRoutesInfoUnsorted = self._scraper.getCragRoutesInfo(url)

        cragRoutesInfo = self._cleaner.sortCragRoutesInfo(cragRoutesInfoUnsorted)

        nameTitleLabel = Label(self._markAscendsWindow, text="Route")
        nameTitleLabel.grid(row=0, column=0, sticky="w")

        gradeTitleLabel = Label(self._markAscendsWindow, text="Grade")
        gradeTitleLabel.grid(row=0, column=1, sticky="w")

        styleTitleLabel = Label(self._markAscendsWindow, text="Type")
        styleTitleLabel.grid(row=0, column=2, sticky="w")

        starsTitleLabel = Label(self._markAscendsWindow, text="Stars")
        starsTitleLabel.grid(row=0, column=3, sticky="w")

        country = self._countryVar.get()
        index = self._resultList.curselection()
        crag = self._resultList.get(index)
        savedRoutesManager = SavedRoutesManager("ascendedRoutes.txt", country, crag)

        self._ascendedRoutes = [] # reset list
        rowCount = 1
        for routeInfo in cragRoutesInfo:
            gradeLabel = Label(self._markAscendsWindow, text=routeInfo[1])
            gradeLabel.grid(row=rowCount, column=1, sticky="w")

            style = routeInfo[2]
            styleLabel = Label(self._markAscendsWindow, text=style)
            styleLabel.grid(row=rowCount, column=2, sticky="w")

            nameVar = IntVar()
            name = routeInfo[0]
            nameLabel = Checkbutton(self._markAscendsWindow, text=name, variable=nameVar, onvalue=1, offvalue=0)
            nameLabel.grid(row=rowCount, column=0, sticky="w")
            ascendedValue = savedRoutesManager.checkIfRouteAscended(name, style)

            if ascendedValue == 1:
                nameLabel.config(fg="green")
                nameVar.set(ascendedValue)

            self._ascendedRoutes.append([name, style, ascendedValue, nameVar])

            stars = str(routeInfo[3])
            if stars == "0.0":
                stars = ""
            else:
                if stars[-1] == "0":
                    stars = stars[0]

            starsLabel = Label(self._markAscendsWindow, text=stars)
            starsLabel.grid(row=rowCount, column=3, sticky="w")

            rowCount += 1

        submitAscends = Button(self._markAscendsWindow, text="Submit", bg="magenta", command=self._registerAscends)
        submitAscends.grid(row=rowCount, column=1, sticky="w")

    def _registerAscends(self):
        country = self._countryVar.get()
        index = self._resultList.curselection()
        crag = self._resultList.get(index)
        routeManager = SavedRoutesManager("ascendedRoutes.txt", country, crag)
        alreadyClimbed = []
        newlyClimbed = []
        for route in self._ascendedRoutes:
            if route[2] == 1:
                alreadyClimbed.append(route)
                continue
            if route[3].get() == 1: # ascended
                name = route[0]; style = route[1]
                newlyClimbed.append([name, style])

        routeManager.registerAscends(newlyClimbed)

    def _getCragUrl(self):
        index = self._resultList.curselection()
        crag = self._resultList.get(index)
        url = self._cragInfo[crag][1]

        return url
    def _getGradeSummary(self):
        url = self._getCragUrl()
        gradeSummary = self._scraper.getGradeInfo(url)

        return gradeSummary

    def _updateCrags(self, event):
        self._scrapeResults()
        self._getResults()

    def _updateCountries(self, event):
        self._setCountries()
        self._scrapeResults()
        self._getResults()

    def _scrapeResults(self):
        country = self._countryVar.get()
        if len(country.split()) != 1:
            country = "-".join(country.split())
        self._cragInfo = self._scraper.getCragInfoForCountry(country)

    def _getResults(self):
        sport = self._styleSportVar.get()
        trad = self._styleTradVar.get()
        boulder = self._styleBoulderVar.get()
        dws = self._styleDwsVar.get()

        allStyles = [sport, trad, boulder, dws]
        selectedStyles = [style for style in allStyles if style]

        results = self._cleaner.getCrags(self._cragInfo, selectedStyles)
        cragNames = []
        for cragInfo in results:
            cragNames.append(cragInfo)
        cragNames.sort()
        self._resultVar.set(cragNames)


    def _setContinent(self):
        self._continent["values"] = ["Europe", "North America", "South America", "Africa", "Asia", "Oceania"]
        self._continent.current(0)

    def _setCountries(self):
        continentRaw = self._continentVar.get()
        if len(continentRaw.split()) == 2:
            continent = "-".join(continentRaw.split())
        else:
            continent = continentRaw
        countries = self._scraper.getCountriesForContinent(continent)
        self._country["values"] = countries
        if continent == "Europe":
            index = countries.index("Norway")
        else:
            index = 0
        self._country.current(index)

master = Tk()
GUI = trackerGUI(master)
master.mainloop()