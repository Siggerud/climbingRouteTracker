class ScrapeCleaner:
    def __init__(self):
        pass

    def sortCragRoutesInfo(self, cragRoutesInfo):
        cragRoutesInfo.sort(key = lambda x: x[1])

        return cragRoutesInfo

    def getCrags(self, cragInfo, climbingStyles):
        if not climbingStyles:
            return cragInfo

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
                for style in climbingStyles:
                    if style in cragStyle:
                        styleCount += 1
                        if styleCount == numOfStyles:
                            cragsThatFitCriteria.append(crag)
                            allStylesFound = True
                            break

        return cragsThatFitCriteria

