class ScrapeCleaner:
    def __init__(self, cragInfo):
        self._cragInfo = cragInfo

    def getCrags(self, climbingStyles):
        if not climbingStyles:
            return self._cragInfo

        cragsThatFitCriteria = []
        numOfStyles = len(climbingStyles)
        for crag, infoList in self._cragInfo.items():
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

