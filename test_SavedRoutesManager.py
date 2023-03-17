from savedRoutesManager import SavedRoutesManager

filename = "testAscendedRoutes.txt"

def _restoreTestText():
    file = open("testAscendedRoutes.txt", "w+")
    file.writelines("country_Section,Norway\n")
    file.writelines("crag_Section,Hauktjern\n")
    file.writelines("Alleen, Partially\n")
    file.writelines("Tassen, Sport\n")
    file.writelines("Mamma mia, Sport\n")
    file.writelines("Ut mot havet, Traditional\n")
    file.writelines("Ungdommens råskap, Sport\n")
    file.writelines("country_Section,Germany\n")
    file.writelines("crag_Section,Spielberg\n")
    file.writelines("El Diente, Sport\n")
    file.writelines("Musikantenstadl, Sport\n")
    file.close()

def test_checkIfCountryIsRegistered():
    manager1 = SavedRoutesManager(filename, "Norway", "Skådalen")
    manager2 = SavedRoutesManager(filename, "Canada", "Rock")

    assert manager1.get_if_country_registered()
    assert not manager2.get_if_country_registered()

def test_checkIfCragIsRegistered():
    manager1 = SavedRoutesManager(filename, "Sweden", "Hauktjern")
    manager2 = SavedRoutesManager(filename, "Germany", "Hauktjern")
    manager3 = SavedRoutesManager(filename, "Germany", "Spielberg")

    assert not manager1.get_if_crag_registered()
    assert not manager2.get_if_crag_registered()
    assert manager3.get_if_crag_registered()

def test_registerAscends():
    manager1 = SavedRoutesManager(filename, "Norway", "Aurekulpen")
    assert manager1.get_if_country_registered()
    manager1.registerAscends([["Batman", "Sport\n"], ["Matrix", "Trad\n"]])
    lines = manager1.get_all_lines()
    cragFound = False
    batmanFound = False
    matrixFound = False
    for line in lines:
        words = line.split(",")
        if "Batman" in words:
            batmanFound = True
        elif "Matrix" in words:
            matrixFound = True
        elif "Aurekulpen\n" in words:
            cragFound = True

    assert cragFound
    assert batmanFound
    assert matrixFound


    manager2 = SavedRoutesManager(filename, "United Kingdom", "Cave")










_restoreTestText()