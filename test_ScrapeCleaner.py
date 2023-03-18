# test_scrapeCleaner.py - for testing class ScrapeCleaner

from scrapeCleaner import ScrapeCleaner

testCragInfo = [['Din diedertur', '5', 'Sport', 0.0], ['Kult Crux', '6a+', 'Sport', 0.0],
                ['Ingen overhengende fare', '6b+', 'Sport', 1.5], ['Løsning i sikte', '6c', 'Sport', 0.0],
                ['Det ordner seg', '6b', 'Sport', 0.0], ['Trappa', '4+', 'Sport', 0.0],
                ['Resistansen', '6b+', 'Sport', 0.0], ['Umulius', '6b', 'Sport', 0.0],
                ['Svidd gummi', '6b+', 'Sport', 0.0], ['Tynn i bunn', '6a+', 'Sport', 0.0],
                ['Tynn i toppen', '6b+', 'Sport', 0.0], ['Listen-stein', '6b+', 'Sport', 0.0],
                ['Listefest', '5+', 'Sport', 0.0], ['Liten diedertur', '5', 'Sport', 0.0],
                ['Fin balanse', '6a', 'Sport', 0.0]]

testDict = {'Filtvet': [[['boulder', '68']], '/crags/filtvet-kirke'], 'Music': [[['sport', '17']], '/crags/rysstad-music'],
            'Hasvåg': [[['boulder', '41']], '/crags/hasvag'], 'Misje': [[['boulder', '34']], '/crags/hella'],
            'Hyggen Main': [[['sport', '57'], ['trad', '8']], '/crags/hyggen'], 'Løkenhavna': [[['sport', '65']], '/crags/lkenhavna'],
            'Skullerudstua': [[['boulder', '72']], '/crags/skullerudstua'], 'Gandalf bouldering': [[['boulder', '21']], '/crags/henningsr-bridge'],
            'Pianokrakken': [[['sport', '1'], ['trad', '17'], ['boulder', '5']], '/crags/pianokrakken'],
            'Godt Levert steinen': [[['boulder', '14']], '/crags/godt-levert-steinen'], 'Sirevåg': [[['boulder', '92']], '/crags/sirevag'],
            'Kuvauen': [[['boulder', '92']], '/crags/kuvauen'], 'Bø': [[['sport', '11'], ['trad', '2']], '/crags/bo'],
            'Hauktjern': [[['sport', '78'], ['trad', '31'], ['boulder', '1'], ['DWS', '5']], '/crags/hauktjern']}

cleaner = ScrapeCleaner()

def test_sort_crag_routesinfo():
    sorted = cleaner.sort_crag_routesinfo(testCragInfo)
    for i in range(1, len(sorted)):
        # checking that routes are sorted by grade
        assert sorted[i][1] >= sorted[i-1][1]

def test_get_crags():
    criteria1 = []
    # check that nothing is filtered when nothing is selected
    assert cleaner.get_crags(testDict, criteria1) == list(testDict.keys())

    # checking that expected filtered results are returned
    criteria2 = ["DWS", "sport"]
    assert cleaner.get_crags(testDict, criteria2) == ["Hauktjern"]

    criteria3 = ["boulder"]
    assert cleaner.get_crags(testDict, criteria3) == ["Filtvet", "Hasvåg", "Misje", "Skullerudstua",
                                                     "Gandalf bouldering", "Pianokrakken", "Godt Levert steinen",
                                                     "Sirevåg", "Kuvauen", "Hauktjern"]

    criteria4 = ["trad", "boulder"]
    assert cleaner.get_crags(testDict, criteria4) == ["Pianokrakken", "Hauktjern"]



