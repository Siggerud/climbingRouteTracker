# test_SavedRoutesManager.py - for testing SavedRoutesManager

from savedRoutesManager import SavedRoutesManager

filename = "testAscendedRoutes.txt"

# for restoring test txt file whenever a test function has changed the file
def restore_test_text():
    file = open("testAscendedRoutes.txt", "w+")
    file.writelines("country_Section,Norway\n")
    file.writelines("crag_Section,Hauktjern\n")
    file.writelines("Alleen,Partially\n")
    file.writelines("Tassen,Sport\n")
    file.writelines("Mamma mia,Sport\n")
    file.writelines("Ut mot havet,Traditional\n")
    file.writelines("Ungdommens råskap,Sport\n")
    file.writelines("country_Section,Germany\n")
    file.writelines("crag_Section,Spielberg\n")
    file.writelines("El Diente,Sport\n")
    file.writelines("Musikantenstadl,Sport\n")
    file.close()

def test_check_if_country_registered():
    manager1 = SavedRoutesManager(filename, "Norway", "Skådalen")
    manager2 = SavedRoutesManager(filename, "Canada", "Rock")

    assert manager1.get_if_country_registered()
    assert not manager2.get_if_country_registered()

def test_check_if_crag_registered():
    manager1 = SavedRoutesManager(filename, "Sweden", "Hauktjern")
    manager2 = SavedRoutesManager(filename, "Germany", "Hauktjern")
    manager3 = SavedRoutesManager(filename, "Germany", "Spielberg")

    assert not manager1.get_if_crag_registered()
    assert not manager2.get_if_crag_registered()
    assert manager3.get_if_crag_registered()

def test_register_ascends():
    manager1 = SavedRoutesManager(filename, "Norway", "Aurekulpen")
    assert manager1.get_if_country_registered()
    manager1.register_ascends([["Batman", "Sport\n"], ["Matrix", "Trad\n"]])
    lines = manager1.get_all_lines()
    cragFound = False
    batmanFound = False
    matrixFound = False
    # check that new routes have been registered
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

    restore_test_text() # reset txt file

    manager2 = SavedRoutesManager(filename, "United Kingdom", "Cave")
    assert not manager2.get_if_country_registered()
    manager2.register_ascends([["Happy feet", "Boulder\n"], ["King Kong", "Sport\n"]])
    lines = manager2.get_all_lines()
    countryFound = False
    cragFound = False
    boulderFound = False
    kingKongFound = False
    for line in lines:
        words = line.split(",")
        if "Boulder\n" in words:
            boulderFound = True
        elif "King Kong" in words:
            kingKongFound = True
        elif "Cave\n" in words:
            cragFound = True
        elif "United Kingdom\n" in words:
            countryFound = True

    assert boulderFound
    assert kingKongFound
    assert cragFound
    assert countryFound

    restore_test_text()

    manager3 = SavedRoutesManager(filename, "Norway", "Hauktjern")
    cragEndStart = manager3.get_crag_end()
    manager3.register_ascends([["Lloyd", "Sport"], ["Cliffhanger", "Trad"]])
    cragEndEnd = manager3.get_crag_end()

    # check that the cragEnd attribute is changed according to number of registered ascends
    assert cragEndStart == cragEndEnd - 2

    restore_test_text()

def test_delete_ascends():
    manager1 = SavedRoutesManager(filename, "Norway", "Hauktjern")
    cragEndStart = manager1.get_crag_end()
    manager1.delete_ascends([["Alleen", "Partially\n"], ["Mamma mia", "Sport\n"]])
    cragEndEnd = manager1.get_crag_end()

    alleenFound = False
    mammamiaFound = False

    lines = manager1.get_all_lines()
    # check if deleted routes are found
    for line in lines:
        words = line.split(",")
        if "Alleen" in words:
            alleenFound = True
        elif "Mamma mia" in words:
            mammamiaFound = True

    assert not alleenFound
    assert not mammamiaFound

    # check that cragEnd attribute is changed according to number of routes deleted
    assert cragEndStart == cragEndEnd + 2

    restore_test_text()

    manager2 = SavedRoutesManager(filename, "Germany", "Spielberg")
    manager2.delete_ascends([["El Diente", "Sport\n"], ["Musikantenstadl", "Sport\n"]])

    elDienteFound = False
    cragFound = False
    countryFound = False

    lines = manager2.get_all_lines()
    for line in lines:
        words = line.split(",")
        if "El Diente" in words:
            elDienteFound = True
        elif "Spielberg\n" in words:
            cragFound = True
        elif "Germany\n" in words:
            countryFound = True

    assert not elDienteFound
    assert not cragFound
    assert not countryFound

    restore_test_text()

def test_check_if_route_ascended():
    manager1 = SavedRoutesManager(filename, "Norway", "Hauktjern")
    assert not manager1.check_if_route_ascended("El Diente", "Sport")
    assert manager1.check_if_route_ascended("Tassen", "Sport")

    manager2 = SavedRoutesManager(filename, "Germany", "Rocks")
    assert not manager2.check_if_route_ascended("El Diente", "Sport")

    manager3 = SavedRoutesManager(filename, "Germany", "Spielberg")
    assert not manager3.check_if_route_ascended("Ut mot havet", "Traditional")
    assert manager3.check_if_route_ascended("Musikantenstadl", "Sport")












restore_test_text()