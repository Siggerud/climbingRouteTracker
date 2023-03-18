class ScrapeCleaner:
    # cleans scraped data from 27crags
    def __init__(self):
        pass

    # sorts crag info based on grade level
    def sort_crag_routesinfo(self, cragRoutesInfo):
        cragRoutesInfo.sort(key = lambda x: x[1])

        return cragRoutesInfo

    # get crags that fits criteria of selected climbing styles
    def get_crags(self, cragInfo, climbingStyles):
        # return all crag info if no styles are selected
        if not climbingStyles:
            return list(cragInfo.keys())

        cragsThatFitCriteria = []
        numOfStyles = len(climbingStyles)
        for crag, infoList in cragInfo.items():
            styleCount = 0
            allStylesFound = False
            for cragStyle in infoList[0]:
                if not cragStyle:
                    break
                if allStylesFound:
                    break
                # check if selected climbing styles are found at crag
                for style in climbingStyles:
                    if style in cragStyle:
                        styleCount += 1
                        if styleCount == numOfStyles:
                            cragsThatFitCriteria.append(crag)
                            allStylesFound = True
                            break

        return cragsThatFitCriteria

