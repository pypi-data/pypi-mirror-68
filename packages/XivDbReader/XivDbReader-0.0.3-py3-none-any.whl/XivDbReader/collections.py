
from uuid import uuid4
from typing import List

class Item():
    def __init__(self):
        self.url: str
        self.pictureUrl: str
        self.name: str
        self.rarity: str
        self.untradable: bool = False
        self.unique: bool = False

        self.itemLevel: int = 0
        self.physicalDamage: int = 0
        self.autoAttack: float = 0.0
        self.delay: float = 0.0

        self.sellPrice: str = ''
        self.buyPrice: str = ''
        self.buyFrom: List = ()
        self.marketProhibited: bool = False
        
        self.patch: str = 'x.x'

class Equipment(Item):
    def __init__(self):
        self.reset()
        pass

    def reset(self):
        self.slot: str = "main"
        self.itemLevel: int = 0
        self.jobs: List = []
        self.level: int = 0

        self.stats = Stats()
        
        self.companyCrest: bool = False
        self.armorie: bool = False
        self.glamourChest: bool = False
        
        self.dyeable: bool
        self.extractable: bool = False
        self.projectable: bool = False
        self.desynth: float = 0.0

        self.repair = RepairInfo()
        self.materia = Materia()

        self.relatedDuties: List = []
        self.requiredItems: List = []
        pass

class Weapon(Equipment):
    def __init__(self):
        self.physicalDamage: int = 0
        self.magicDamage: int = 0
        self.autoAttack: float = 0.0
        self.delay: float = 0.0

    def getCsvHeader(self) -> List[str]:
        header: str = [
            'key'
            ,'url'
            ,'pictureUrl'
            ,'name'
            ,'rarity'
            ,'untradeable'
            ,'unique'
            ,'slot'
            ,'itemLevel'
            ,'jobs'
            ,'level'
            ,'companyCrest'
            ,'armorie'
            ,'glamourChest'
            ,'dyeable'
            ,'extractable'
            ,'projectable'
            ,'desynth'
            ,'patch'
        ]
        return header
    
    def getCsvRow(self) -> List[str]:
        self.key = uuid4()
        row: List[str] = [
            str(self.key)
            ,self.url
            ,self.pictureUrl
            ,self.name
            ,self.rarity
            ,self.untradable
            ,self.unique
            ,self.slot
            ,self.itemLevel
            ,self.jobs
            ,self.level
            ,self.companyCrest
            ,self.armorie
            ,self.glamourChest
            ,self.dyeable
            ,self.extractable
            ,self.projectable
            ,self.desynth
            ,self.patch
        ]
        return row

        
class Armor(Equipment):
    def __init__(self):
        self.defense: int = 0
        self.magicDefense: int = 0

class Tool():
    pass


class RepairInfo():
    """
    About: Describes the what is required to repair a item
    """

    def __init__(self):
        self.job: str = ''
        self.level: int = 0
        self.material: str = ''
        pass

    def getCsvHeader(self) -> List[str]:
        return ['key', 'job', 'level', 'material']

    def getCsvRow(self) -> List[str]:
        key = uuid4()
        return [key, self.job, self.level, self.material]

class Materia():
    def __init__(self):
        self.slots: int = 0
        self.melderJob: str = ''
        self.melderLevel: int = 0
        self.advancedMelding: bool = True
        pass

    def getCsvHeader(self) -> List[str]:
        header = ['key','slots', 'melderJob', 'melderLevel','advancedMelding']
        return header
    
    def getCsvRow(self) -> List[str]:
        key = uuid4()
        row = [key, self.slots, self.melderJob, self.melderLevel, self.advancedMelding]
        return row

class Stats():
    def __init__(self):
        self.strength: int = 0        
        self.vitality: int = 0
        self.dexterity: int = 0
        self.intelligence: int = 0
        self.mind: int = 0

        self.determination: int = 0
        self.skillSpeed: int = 0
        self.spellSpeed: int = 0
        self.criticalHit: int = 0
        self.directHitRate: int = 0
        self.tenacity: int = 0
        self.piety: int = 0
        pass

    def getCsvHeader(self) -> List[str]:
        return ['key', 'strength', 'vitality', 'dexterity', 'intelligence',
            'mind', 'determination', 'skillSpeed', 'spellSpeed', 'criticalHit',
            'directHitRate', 'tenacity', 'piety']

    def getCsvRow(self) -> List[str]:
        key = uuid4()
        return [key, self.strength, self.vitality, self.dexterity, self.intelligence,
        self.mind, self.determination, self.skillSpeed, self.spellSpeed, self.criticalHit,
        self.directHitRate, self.tenacity, self.piety]

class ExchangeItems():
    def __init__(self):
        self.name: str = ''
        self.amount: int = 0
        pass

class ExchangeFor():
    def __init__(self):
        self.items: List[ExchangeItems] = []
        self.npc: str = ""
        self.location: str = ""

class DropsFrom():
    def __init__(self):
        self.type: str = ''
        self.expansion: str = ''
        self.name: str = ''
        self.level: int = 0
        self.itemLevel: int = 0
        
    def getCsvHeader(self) -> List[str]:
        return ['key', 'type', 'expansion', 'name', 'level', 'itemLevel']
    
    def getCsvRow(self) -> List[str]:
        key = uuid4()
        return [key, self.type, self.expansion, self.name, self.level, self.itemLevel]

class Value():
    def __init__(self):
        self.buy: int = 0
        self.sell: int = 0
        self.sellOnMarket: bool = True
        self.unsellable: bool = False
        self.buyFrom: List[Vendors] = []

class Vendors():
    def __init__(self):
        self.name: str = ''
        self.location: str = ''
