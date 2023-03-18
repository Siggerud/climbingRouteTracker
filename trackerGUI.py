from tkinter import Tk, ttk, StringVar, Checkbutton, Listbox, Variable, Frame, Label, \
    Toplevel, Button, IntVar, Canvas
from scraper import CragScraper
from scrapeCleaner import ScrapeCleaner
from savedRoutesManager import SavedRoutesManager

class TrackerGUI:
    # creates a GUI for tracking climbed routes
    def __init__(self, master):
        self._master = master
        self._master.geometry("300x450")
        self._master.title("Climbing routes tracker")

        self._biggerSizeFont = ("Helvetica", 10)
        self._font = ("Helvetica", 9)
        self._padx = 5
        comboWidth = 10

        self._cragInfo = []
        self._routesAtCrag = []
        self._scraper = CragScraper()
        self._cleaner = ScrapeCleaner()

        self._continentVar = StringVar()
        self._continent = ttk.Combobox(self._master, font=self._font, textvariable=self._continentVar, width=comboWidth)
        self._continent.place(x=10, y=10)
        # set the continents registered on 27crags
        self._set_continents()
        # update countries whenever a new continent is chosen
        self._continent.bind("<<ComboboxSelected>>", self._update_countries)

        self._countryVar = StringVar()
        self._country = ttk.Combobox(self._master, font=self._font, textvariable=self._countryVar, width=comboWidth)
        self._country.place(x=10, y=40)
        # set the countries for default continent
        self._set_countries_for_continent()
        # update crags whenever a new country is chosen
        self._country.bind("<<ComboboxSelected>>", self._update_crags)

        # define checkboxes for type of climb
        self._styleSportVar = StringVar()
        self._styleSport = Checkbutton(self._master, text="Sport", font=self._font, variable=self._styleSportVar,
                                       onvalue="sport", offvalue="", command=self._get_results)
        self._styleSport.place(x=5, y=70)

        self._styleTradVar = StringVar()
        self._styleTrad = Checkbutton(self._master, text="Trad", font=self._font, variable=self._styleTradVar,
                                      onvalue="trad", offvalue="", command=self._get_results)
        self._styleTrad.place(x=65, y=70)

        self._styleBoulderVar = StringVar()
        self._styleBoulder = Checkbutton(self._master, text="Boulder", font=self._font, variable=self._styleBoulderVar,
                                         onvalue="boulder", offvalue="", command=self._get_results)
        self._styleBoulder.place(x=125, y=70)

        self._styleDwsVar = StringVar()
        self._styleDws = Checkbutton(self._master, text="DWS", font=self._font, variable=self._styleDwsVar,
                                     onvalue="DWS", offvalue="", command=self._get_results)
        self._styleDws.place(x=5, y=95)

        # the list showing all crags
        self._resultVar = Variable()
        self._resultList = Listbox(self._master, font=self._font, listvariable=self._resultVar, height=15)
        self._resultList.place(x=5, y=125)

        # get crags and related info for default country
        self._scrape_crag_info_for_country()
        self._get_results()
        # show info on crag whenever a crag is clicked
        self._resultList.bind('<<ListboxSelect>>', self._show_crag_gradeinfo)

        self._cragGradeInfoFrame = Frame(self._master)
        self._cragGradeInfoFrame.place(x=150, y=125)

    # shows info on grades for crag
    def _show_crag_gradeinfo(self, event):
        # do nothing if nothing is selected
        if self._resultList.curselection() == ():
            return

        # destroy any old widgets
        for widget in self._cragGradeInfoFrame.winfo_children():
            widget.destroy()

        cragGradeLabel = Label(self._cragGradeInfoFrame, text="Grade", font=self._biggerSizeFont)
        cragGradeLabel.grid(row=0, column=0, sticky="w", padx=self._padx)

        cragNumberLabel = Label(self._cragGradeInfoFrame, text="Number", font=self._biggerSizeFont)
        cragNumberLabel.grid(row=0, column=1, sticky="w", padx=self._padx)

        gradeSummary = self._get_grade_summary()
        rowCount = 1
        # add all the grades found for crag
        for grade, number in gradeSummary.items():
            gradeLabel = Label(self._cragGradeInfoFrame, text=grade, font=self._font)
            gradeLabel.grid(row=rowCount, column=0, sticky="w", padx=self._padx)

            numberLabel = Label(self._cragGradeInfoFrame, text=number, font=self._font)
            numberLabel.grid(row=rowCount, column=1, sticky="w", padx=self._padx)

            rowCount += 1

        markButton = Button(self._cragGradeInfoFrame, text="Mark ascents", font=self._font, bg="springgreen", command=self._make_popup)
        markButton.grid(row=rowCount, column=0, sticky="w", columnspan=2)

    # creates a popup window when we want to register ascends
    def _make_popup(self):
        self._markAscendsWindow = Toplevel(self._master)
        self._markAscendsWindow.title("Mark ascents")
        self._markAscendsWindow.geometry("400x500")

        # get info on each route on selected crag
        url = self._get_crag_url()
        cragRoutesInfoUnsorted = self._scraper.get_crag_routesinfo(url)
        cragRoutesInfo = self._cleaner.sort_crag_routesinfo(cragRoutesInfoUnsorted)

        # frame to contain canvas and scrollable frame
        self._containerFrame = ttk.Frame(self._markAscendsWindow)

        self._routeCanvas = Canvas(self._containerFrame)

        # scrollable frame
        routeSroll = ttk.Scrollbar(self._containerFrame, orient="vertical", command=self._routeCanvas.yview)

        self._routeInfoFrame = Frame(self._routeCanvas)
        # set up the scrollbar
        self._routeInfoFrame.bind("<Configure>",
                                  lambda e: self._routeCanvas.configure(
                                      scrollregion=self._routeCanvas.bbox("all")
                                  ))

        self._routeCanvas.create_window((0,0), window=self._routeInfoFrame, anchor="nw")
        self._routeCanvas.configure(yscrollcommand=routeSroll.set)

        # add title labels
        nameTitleLabel = Label(self._routeInfoFrame, text="Route", font=self._biggerSizeFont)
        nameTitleLabel.grid(row=0, column=0, sticky="w")

        gradeTitleLabel = Label(self._routeInfoFrame, text="Grade", font=self._biggerSizeFont)
        gradeTitleLabel.grid(row=0, column=1, sticky="w", padx=self._padx)

        styleTitleLabel = Label(self._routeInfoFrame, text="Type", font=self._biggerSizeFont)
        styleTitleLabel.grid(row=0, column=2, sticky="w", padx=self._padx)

        starsTitleLabel = Label(self._routeInfoFrame, text="Stars", font=self._biggerSizeFont)
        starsTitleLabel.grid(row=0, column=3, sticky="w", padx=self._padx)

        country = self._countryVar.get()
        crag = self._get_selected_crag()
        savedRoutesManager = SavedRoutesManager("ascendedRoutes.txt", country, crag)

        self._routesAtCrag = [] # reset list
        rowCount = 1
        # add info on each route
        for routeInfo in cragRoutesInfo:
            gradeLabel = Label(self._routeInfoFrame, text=routeInfo[1], font=self._font)
            gradeLabel.grid(row=rowCount, column=1, sticky="w", padx=self._padx)

            style = routeInfo[2]
            styleLabel = Label(self._routeInfoFrame, text=style, font=self._font)
            styleLabel.grid(row=rowCount, column=2, sticky="w", padx=self._padx)

            nameVar = IntVar()
            name = routeInfo[0]
            nameLabel = Checkbutton(self._routeInfoFrame, text=name, font=self._font, variable=nameVar, onvalue=1, offvalue=0)
            nameLabel.grid(row=rowCount, column=0, sticky="w")
            # check if route is already climbed
            ascended = savedRoutesManager.check_if_route_ascended(name, style)
            if ascended:
                ascendedValue = 1
            else:
                ascendedValue = 0

            if ascendedValue == 1:
                # mark route as already climbed
                nameLabel.config(fg="green")
                nameVar.set(ascendedValue)

            self._routesAtCrag.append([name, style, ascendedValue, nameVar])

            stars = str(routeInfo[3])
            if stars == "0.0":
                # write nothing if no stars for route
                stars = ""
            else:
                if stars[-1] == "0":
                    # drop .0 decimal
                    stars = stars[0]

            starsLabel = Label(self._routeInfoFrame, text=stars, font=self._font)
            starsLabel.grid(row=rowCount, column=3, sticky="w", padx=self._padx)

            rowCount += 1

        self._containerFrame.pack()
        self._routeCanvas.pack(side="left", fill="both", expand=True)
        routeSroll.pack(side="right", fill="y")

        submitAscends = Button(self._markAscendsWindow, text="Submit", font=self._font, bg="magenta",
                               command=self._register_ascends)
        submitAscends.pack()

    # registers ascended routes
    def _register_ascends(self):
        country = self._countryVar.get()
        crag = self._get_selected_crag()
        routeManager = SavedRoutesManager("ascendedRoutes.txt", country, crag)
        alreadyClimbed = []
        newlyClimbed = []
        for route in self._routesAtCrag:
            if route[2] == 1 and route[3].get() == 0:
                # unselected route previously marked as climbed
                name = route[0]; style = route[1]
                alreadyClimbed.append([name, style + "\n"])
            elif route[2] == 0 and route[3].get() == 1:
                # selected new route as climbed
                name = route[0]; style = route[1]
                newlyClimbed.append([name, style + "\n"])

        # registers any new ascends
        routeManager.register_ascends(newlyClimbed)
        # removes previous ascends
        if alreadyClimbed:
            routeManager.delete_ascends(alreadyClimbed)

        # close window when submitted
        self._markAscendsWindow.destroy()

    # get url for selected crag
    def _get_crag_url(self):
        crag = self._get_selected_crag()
        url = self._cragInfo[crag][1]

        return url

    # get crag selected in listbox
    def _get_selected_crag(self):
        index = self._resultList.curselection()
        crag = self._resultList.get(index)

        return crag

    # retrieves a summary of grades for crag
    def _get_grade_summary(self):
        url = self._get_crag_url()
        gradeSummary = self._scraper.get_gradeinfo(url)

        return gradeSummary

    # gets info and updates the crags in the resultlist
    def _update_crags(self, event):
        self._scrape_crag_info_for_country()
        self._get_results()

    # updates the countries in combobox
    def _update_countries(self, event):
        self._set_countries_for_continent()
        self._scrape_crag_info_for_country()
        self._get_results()

    # gets info on crags for country selected
    def _scrape_crag_info_for_country(self):
        country = self._countryVar.get()
        if len(country.split()) != 1:
            country = "-".join(country.split())
        self._cragInfo = self._scraper.get_crag_info_for_country(country)

    # sets crags in listbox based on ticked checkboxes
    def _get_results(self):
        sport = self._styleSportVar.get()
        trad = self._styleTradVar.get()
        boulder = self._styleBoulderVar.get()
        dws = self._styleDwsVar.get()

        allStyles = [sport, trad, boulder, dws]
        selectedStyles = [style for style in allStyles if style] # only get selected styles

        results = self._cleaner.get_crags(self._cragInfo, selectedStyles)
        cragNames = []
        for crag in results:
            # skip crags with no known routes
            if self._cragInfo[crag][0]:
                cragNames.append(crag)
        cragNames.sort() # sort crags alphabetically
        self._resultVar.set(cragNames)

    # set continent combobox with continents registered on 27crags
    def _set_continents(self):
        self._continent["values"] = ["Europe", "North America", "South America", "Africa", "Asia", "Oceania"]
        self._continent.current(0)

    # sets the countries for default continent at startup
    def _set_countries_for_continent(self):
        continent = self._get_continent()
        countries = self._get_countries_for_continent(continent)
        self._country["values"] = countries
        if continent == "Europe":
            index = countries.index("Norway")
        else:
            index = 0
        self._country.current(index)

    # get selected continet in scraping friendly from
    def _get_continent(self):
        continentRaw = self._continentVar.get()
        if len(continentRaw.split()) == 2:
            continent = "-".join(continentRaw.split())
        else:
            continent = continentRaw

        return continent

    # retrieves all countries registered for selected continent at 27crags
    def _get_countries_for_continent(self, continent):
        countriesForContinent = self._scraper.get_countries_for_continent(continent)

        return countriesForContinent

master = Tk()
GUI = TrackerGUI(master)
master.mainloop()