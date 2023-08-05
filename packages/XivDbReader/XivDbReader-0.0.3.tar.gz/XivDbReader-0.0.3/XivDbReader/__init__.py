
from .settings import *
from .collections import *
from XivDbReader.scrape import ParseList, ParseItems
from typing import List
import os
import csv
import uuid

class ExportCsv():
    def __init__(self, recordType: str, recordJob: str, replaceFiles: bool = True):
        self.recordType: str = recordType
        self.recordJob: str = recordJob
        self.__updateFileName__()
        #self.fileName: str = f"{recordType}_{recordJob}.csv"
        self.replaceFiles: bool = replaceFiles
        pass

    def write(self, objectList: List) -> None:
        # Check if file already exists
        recordType = self.recordType
        if self.replaceFiles == True:
            self.__removeExistingFile__()
            pass

        for i in objectList:
            o = i
            t: str = str(type(o))
            if 'weapon' in t.lower():
                w: Weapon = i
                self.__writeWeapon__(w, recordType)
                self.__writeWeapon__(w.stats, f'{recordType}_stats')
                self.__writeWeapon__(w.materia, f'{recordType}_materia')
                self.__writeWeapon__(w.repair, f'{recordType}_repair')

    def __writeWeapon__(self, w: Weapon, recordType) -> None:
        self.recordType = recordType
        self.__updateFileName__()
        if os.path.exists(self.fileName) == False:
            self.__writeLine__(w.getCsvHeader())
        self.__writeLine__(w.getCsvRow())


    def __updateFileName__(self) -> None:
        self.fileName = f"{self.recordType}_{self.recordJob}.csv"

    def __writeLine__(self, line) -> None:
        with open(self.fileName, 'a', newline='') as csvfile:
            try:
                writecvs = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writecvs.writerow(line)
            except Exception as e:
                print(f"ERROR - {e}")

    def __removeExistingFile__(self) -> None:
        try:
            exists = os.path.exists(self.fileName)
            if exists == True:
                os.remove(f"{self.fileName}")
        except Exception as e:
            print(f"ERROR - {e}")
    

class Reader():
    def __init__(self, job: str):
        self.job = job
        pass

    def getArms(self, recordLimit: int = -1) -> List[Weapon]:
        self.recordLimit = recordLimit
        weapons: List[Weapon] = []
        s = Settings()
        link = s.links.getArmLink(job=self.job)
        
        page: int = 0
        loopKeeper: bool = False
        # Get the items from the list

        while loopKeeper == False:
            res = self.__extractInfo__(f"{link}&page={page}")
            if res.__len__() == 0:
                loopKeeper = True
                break
            else:
                for i in res:
                    weapons.append(i)
                page = page + 1
                if weapons.__len__() == self.recordLimit:
                    break

        self.recordLimit = -1
        return weapons

    def getArmor(self, slot: str, recordLimit: int = -1) -> List[Armor]:
        self.recordLimit = recordLimit
        armors: List[Armor] = []
        s = Settings()
        link = s.links.getArmorLink(slot)
        page:int = 0
        loopKeeper: bool = False
        while loopKeeper == False:
            res = self.__extractInfo__(f"{link}&page={page}")
            if res.__len__() == 0:
                loopKeeper = True
                break
            else:
                armors.append(res)
                page = page + 1
                if armors.__len__() == self.recordLimit:
                    break

        self.recordLimit = -1
        return armors

    def __extractInfo__(self, link: str) -> List[Item]:
        itemsList: List[Item] = []
        pl = ParseList(link)
        items: List[str] = pl.FindLinks()

        for item in items:
            pi = ParseItems()
            details: Item = pi.getDetails(href=item)
            itemsList.append(details)
            print(f"INFO - Got info on '{details.name}'")
            if itemsList.__len__() == self.recordLimit:
                break
        
        return itemsList

