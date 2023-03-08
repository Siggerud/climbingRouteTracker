from bs4 import BeautifulSoup
import requests
from threading import Thread

# TODO: find a way to scrape dynamic pages


class CragScraper:
    def __init__(self):
        self._baseUrl = "https://27crags.com"
        self._crags = []

    def _getSoup(self, url):
        response = requests.get(self._baseUrl + url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        return soup

    def _getSoupAfterJavascript(self, url):
        # skriv selenium kode her

    def getCountriesForContinent(self, continent):
        countries = []
        soup = self._getSoup("/continents/" + continent)
        countryTags = soup.find_all("a", class_="sector-item")
        for tag in countryTags:
            countries.append(tag.text.strip())
        return countries

    def _getLastPage(self, soup):
        navTag = soup.find("ul", role="navigation")
        lastPage = int(navTag.find_all("li")[-2].text)

        return lastPage

    def getCragsForCountry(self, country):
        soup = self._getSoup("/countries/" + country.lower())
        lastPage = self._getLastPage(soup)

        trimmingThreads = []
        for i in range(0, lastPage +1, 1):
            start = i
            end = i+1
            if start == 0:
                start = 1
            trimmingThread = Thread(target=self._threadedGetCragsForCountry, args=(country, start, end))
            trimmingThreads.append(trimmingThread)
            trimmingThread.start()

        for thread in trimmingThreads:
            thread.join()

    def _threadedGetCragsForCountry(self, country, start, end):
        for i in range(start, end):
            url = f"/countries/{country}/descending/by/favourite_count/page/{i}"
            soup = self._getSoupAfterJavascript(url)
            cragTags = soup.find_all("div", class_="crag-summary")
            for tag in cragTags:
                info = []
                name = tag.find("div", class_="crag-name").text
                typesOfRoutesTag = tag.find_all("span", class_="route-count")
                for elem in typesOfRoutesTag:
                    if not elem.is_empty_element:
                        try:
                            typeOfRoute = elem.find("span", class_="name").text.strip()
                        except:
                            continue
                        numberOfRoutes = elem.find("i").next.text.strip()
                        routeInfo = [typeOfRoute, numberOfRoutes]
                        info.append(routeInfo)

                spanTags = tag.find_all("span", class_="cell")
                for spanTag in spanTags:
                    numberOfGrade = spanTag.next.text
                    print(numberOfGrade)

                info.append(name)
                self._crags.append(info)





