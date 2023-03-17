from bs4 import BeautifulSoup
import requests
from threading import Thread
from requests_html import HTMLSession

# TODO: find a way to scrape dynamic pages


class CragScraper:
    def __init__(self):
        self._baseUrl = "https://27crags.com"
        self._cragInfo = {}

    def getCragRoutesInfo(self, url):
        soup = self._getSoup(url + "/routelist")
        cragTags = soup.find_all("td", class_="txt")
        cragRoutesInfo = []
        for cragTag in cragTags:
            name = cragTag.find("a", class_="lfont").text
            grade, style = cragTag.find("div", class_="visible-xs-block").text.strip().split()[0:2]
            starTag = cragTag.find("span", class_="stars")
            fullStars = len(starTag.find_all("div", class_="star full glyphicon glyphicon-star"))
            halfStars = len(starTag.find_all("div", class_="star half glyphicon glyphicon-star-empty"))
            numberOfStars = fullStars - 0.5 * halfStars
            temp = [name, grade, style, numberOfStars]
            cragRoutesInfo.append(temp)

        return cragRoutesInfo

    def _getSoup(self, url, dynamic=False):
        if dynamic:
            session = HTMLSession()
            response = session.get(self._baseUrl + url)
            response.html.render()
            soup = BeautifulSoup(response.html.raw_html, "html.parser")
        else:
            response = requests.get(self._baseUrl + url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

        return soup

    def getGradeInfo(self, cragUrl):
        soup = self._getSoup(cragUrl, dynamic=True)
        gradeSummary = soup.find("div", class_="crag-summary summary-big")
        spanTags = gradeSummary.find_all("span", class_="cell")

        gradeSummary = {}
        for tag in spanTags:
            numOfRoutes = tag.next.text
            if numOfRoutes == "":
                continue

            grade = tag.find("span")["title"]
            gradeSummary[grade] = numOfRoutes

        return gradeSummary

    def getCountriesForContinent(self, continent):
        countries = []
        soup = self._getSoup("/continents/" + continent)
        countryTags = soup.find_all("a", class_="sector-item")
        for tag in countryTags:
            countries.append(tag.text.strip())

        return countries

    def _getLastPage(self, soup):
        navTag = soup.find("ul", role="navigation")
        if navTag == None: # if only one page
            lastPage = 1
        else:
            lastPage = int(navTag.find_all("li")[-2].text)

        return lastPage

    def getCragInfoForCountry(self, country):
        self._cragInfo = {} # reset dict
        soup = self._getSoup("/countries/" + country.lower())
        lastPage = self._getLastPage(soup)
        trimmingThreads = []
        for i in range(1, lastPage +1, 1):
            start = i
            end = i+1
            trimmingThread = Thread(target=self._threadedGetCragInfoForCountry, args=(country, start, end))
            trimmingThreads.append(trimmingThread)
            trimmingThread.start()

        for thread in trimmingThreads:
            thread.join()

        return self._cragInfo

    def _threadedGetCragInfoForCountry(self, country, start, end):
        for i in range(start, end):
            url = f"/countries/{country}"
            if i != 1:
                url += f"/descending/by/favourite_count/page/{i}"
            soup = self._getSoup(url)
            cragTags = soup.find_all("div", class_="crag-summary")
            for tag in cragTags:
                cragInfo = []
                name = tag.find("div", class_="crag-name").text
                typesOfRoutesTag = tag.find_all("span", class_="route-count")
                routeInfo = []
                for elem in typesOfRoutesTag:
                    temp = []
                    if not elem.is_empty_element:
                        try:
                            typeOfRoute = elem.find("span", class_="name").text.strip()
                        except:
                            continue
                        numberOfRoutes = elem.find("i").next.text.strip()
                        temp.append(typeOfRoute)
                        temp.append(numberOfRoutes)
                        routeInfo.append(temp)
                cragInfo.append(routeInfo)
                link = tag.parent.parent["href"]
                cragInfo.append(link)

                self._cragInfo[name] = cragInfo






