 
#from XivDbReader.Reader import Reader
from XivDbReader import Reader

def test_armsPld():
    
    r = Reader(job='pld')
    res = r.getArms(recordLimit=1)
    #res = r.getArms('Pld',1)
    if res.__len__() == 1:
        assert True

def test_armsWar():
    r = Reader(job='war')
    res = r.getArms(recordLimit=1)
    if res.__len__() == 1:
        assert True
