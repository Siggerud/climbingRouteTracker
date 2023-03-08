from tkinter import Tk, ttk, StringVar, Checkbutton, IntVar
from scraper import CragScraper

class trackerGUI:
    def __init__(self, master):
        self._master = master
        self._master.geometry("300x300")
        self._master.title("Climbing routes tracker")

        self._continentVar = StringVar()
        self._continent = ttk.Combobox(self._master, textvariable=self._continentVar, width=10)
        self._continent.place(x=10, y=10)

        self._setContinent()

        self._countryVar = StringVar()
        self._country = ttk.Combobox(self._master, textvariable=self._countryVar, width=10)
        self._country.place(x=10, y=40)

        self._setCountries()

        self._styleSportVar = IntVar()
        self._styleSport = Checkbutton(self._master, text="Sport", variable=self._styleSportVar,
                                       onvalue=1, offvalue=0)
        self._styleSport.place(x=5, y=70)

        self._styleTradVar = IntVar()
        self._styleTrad = Checkbutton(self._master, text="Trad", variable=self._styleTradVar,
                                       onvalue=1, offvalue=0)
        self._styleTrad.place(x=65, y=70)

        self._styleBoulderVar = IntVar()
        self._styleBoulder = Checkbutton(self._master, text="Boulder", variable=self._styleBoulderVar,
                                      onvalue=1, offvalue=0)
        self._styleBoulder.place(x=125, y=70)

        self._styleDwsVar = IntVar()
        self._styleDws = Checkbutton(self._master, text="DWS", variable=self._styleDwsVar,
                                      onvalue=1, offvalue=0)
        self._styleDws.place(x=5, y=95)




    def _setContinent(self):
        self._continent["values"] = ["Europe", "North America", "South America", "Africa", "Asia", "Oceania"]
        self._continent.current(0)

    def _setCountries(self):
        scraper = CragScraper()
        continentRaw = self._continentVar.get()
        if len(continentRaw) == 2:
            continent = "-".join(continentRaw.split())
        else:
            continent = continentRaw

        countries = scraper.getCountriesForContinent(continent)
        self._country["values"] = countries
        if continent == "Europe":
            index = countries.index("Norway")
        else:
            index = 0
        self._country.current(index)

master = Tk()
GUI = trackerGUI(master)
master.mainloop()