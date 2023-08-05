


class Settings():
    def __init__(self):
        self.sleepTimer: int = 5

        self.links = Links()

class Links():
    def __init__(self):
        self.rootUrl = "https://na.finalfantasyxiv.com"
        self.dbUrl = f"{self.rootUrl}/lodestone/playguide/db"
        
        self.armsAllUrl = f"{self.dbUrl}/item/?category2=1"       
        self.toolsAllUrl = f"{self.dbUrl}/item/?category2=2"
        self.armorAllUrl = f"{self.dbUrl}/item/?category2=3"
        self.accessoriesAllUrl = f"{self.dbUrl}/item/?category2=4"
        self.medsAllUrl = f"{self.dbUrl}/item/?category2=5&category3=44"
        self.foodAllUrl = f"{self.dbUrl}/item/?category2=5&category3=46"
        self.materialsAllUrl = f"{self.dbUrl}/item/?category2=6"

    def getArmLink(self, job: str) -> str:
        """
        About:
            This will generate links to check based off values given.

        Params:

        """

        cat = -1
        if 'gld' in job or 'pld' in job:
            cat = 2
        elif 'mrd' in job or 'war' in job:
            cat = 3
        elif 'drk' in job:
            cat = 87
        elif 'gnb' in job:
            cat = 106
        elif 'lnc' in job or 'drg' in job:
            cat = 5
        elif 'pug' in job or 'mnk' in job:
            cat = 1
        elif 'sam' in job:
            cat = 96
        elif 'rog' in job or 'nin' in job:
            cat = 84
        elif 'arc' in job or 'brd' in job:
            cat = 4
        elif 'mch' in job:
            cat = 88
        elif 'dnc' in job:
            cat = 107
        elif 'thm' in job:
            cat = 6
        elif 'blm' in job:
            cat = 7
        elif 'acn' in job or 'smn' in job:
            cat = 10
        elif 'rdm' in job:
            cat = 97
        elif 'blu' in job:
            cat = 105
        elif 'cnj' in job:
            cat = 8
        elif 'whm' in job:
            cat = 9
        elif 'sch' in job:
            cat = 98
        elif 'ast' in job:
            cat = 89
        else:
            raise Exception("Invalid job requested")

        link: str = f"{self.armsAllUrl}&category3={cat}"
        return link
        
    def getArmorLink(self, slot: str) -> str:
        
        cat3: int = 0
        if 'shield' in slot.lower():
            cat3 = 11
        elif 'head' in slot.lower():
            cat3 = 34
        elif 'body' in slot.lower():
            cat3 = 35
        elif 'hands' in slot.lower():
            cat3 = 37
        elif 'waist' in slot.lower():
            cat3 = 39
        elif 'legs' in slot.lower():
            cat3 = 36
        elif 'feet' in slot.lower():
            cat3 = 38
        else:
            raise Exception("Invalid slot requested.")
        
        link: str = f"{self.armorAllUrl}&category3={cat3}"
        return link

    def getAccessoryLink(self, slot: str) -> str:
        slot = slot.lower()
        cat3: int = 0
        if 'earring' in slot or 'ear' in slot:
            cat3 = 41
        elif 'necklace' in slot or 'neck' in slot:
            cat3 = 40
        elif 'bracelet' in slot or 'wrist' in slot:
            cat3 = 42
        elif 'ring' in slot:
            cat3 = 43
        elif 'soulstone' in slot or 'stone' in slot:
            cat3 = 62
        else:
            raise Exception("Invalid slot requested.")
        
        link: str = f"{self.accessoriesAllUrl}&category3={cat3}"
        return link
