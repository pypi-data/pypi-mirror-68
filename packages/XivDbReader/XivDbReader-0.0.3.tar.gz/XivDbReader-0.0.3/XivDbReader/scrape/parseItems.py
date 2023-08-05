
from XivDbReader.collections import Item, Weapon, Armor, RepairInfo, Materia, Stats, ExchangeFor, ExchangeItems, DropsFrom, Vendors, Value
from XivDbReader.exceptions import UnableToFindValue

from typing import Dict, List
from bs4 import BeautifulSoup, Tag, ResultSet
import re
import requests

class ParseItems():
    def __init__(self):
        self.soup: BeautifulSoup
        pass

    def GetHtmlSource(self, href: str) -> str:
        self.href = href
        return requests.get(href)

    def getDetails(self, href:str = '', html: str = '') -> Item:
        if html == '':
            if href == '':
                raise Exception("Submit a valid url to getWeaponDetails(href='www....)")
            html: str = requests.get(href)

        self.item = Item()

        soup: BeautifulSoup = BeautifulSoup(html.text, 'html.parser')
        self.soup = soup

        itemText = soup.find_all('div', class_='db-view__item__text')
        innerText = itemText[0].contents[1]

        unique: bool = False
        untradable: bool = False
        name: str = ''
        rarity: str = ''

        try:
            innerText = soup.find_all('div', class_='db-view__item__text__inner')
            for i in innerText[0].contents:
                if i == '\n':
                    continue

                # Gets what slot the item goes to
                #if i.attrs['class'][0] == 'db-view__item__text__name':
                #    slot = i.text
                #    continue

                if innerText[0].contents[1].attrs['class'][0] == '':
                    pass

                # i.attrs['class'][0]
                #'db-view__item__text__element'
                if i.attrs['class'][0] == 'db-view__item__text__element':
                    for rareType in i.contents:
                        if rareType == '\n':
                            continue

                        if rareType.text == 'Unique':
                            unique = True
                            continue
                        
                        if rareType.text == 'Untradable':
                            untradable = True
                            continue
                    continue

                if i.attrs['class'][0] == 'db-view__item__storage':
                    for g in i.contents:
                        if g == '\n':
                            continue

                        alt = g.contents[0].attrs['alt']
                        if "company crests" in alt:
                            if "Cannot" in alt: 
                                companyCrest = False
                                continue
                            else: 
                                companyCrest = True
                                continue
                        
                        if "dresser" in alt:
                            if "Cannot" in alt: 
                                glamourChest = False
                                continue
                            else: 
                                glamourChest = True
                                continue
                        
                        if "armoire" in alt: 
                            if "Cannot" in alt: 
                                armorie = False
                                continue
                            else: 
                                armorie = True
                                continue
                    continue

                # Gets the name of the time
                if i.attrs['class'][0] == 'db-view__item__text__name':
                    name = i.text
                    name = name.replace('\n', '')
                    name = name.replace('\t', '')
                    name = name.replace('\ue03c', '')
                    name = name

                    rarity = i.attrs['class'][1]
                    if "uncommon" in rarity:
                        rarity = "Uncommon"
                    elif "common" in rarity:
                        rarity = "Common"
                    elif "rare" in rarity:
                        rarity = "Rare"
                    elif "epic" in rarity:
                        rarity = "Epic"

                    slot = name
                    continue

                if i.attrs['class'][0] == 'db-view__item__text__category':
                    slot = i.text

        except Exception as e:
            print(e)
            pass

        if slot == "Shield" or \
            slot == "Head" or \
            slot == "Body" or \
            slot == 'Hands' or \
            slot == "Waist" or \
            slot == "Legs" or \
            slot == "Feet":

            self.item = Armor()
        elif "Arm" in slot or \
            "Grimoire" in slot:
            self.item = Weapon()

        self.item.repair = RepairInfo()
        self.item.materia = Materia()
        self.item.stats = Stats()
        self.item.vendors = Value()

        self.item.name = name
        self.item.slot = slot
        self.item.rarity = rarity
        self.item.unique = unique
        self.item.untradable = untradable
        self.item.url = href
        self.item.companyCrest = companyCrest
        self.item.glamourChest = glamourChest
        self.item.armorie = armorie

        # Find what patch we are reviewing data for
        self.patchVersion()

        itemLevel: str = soup.find_all('div', class_='db-view__item_level')[0].text
        self.item.itemLevel: int = int(itemLevel.replace('Item Level ', ''))

        self.itemPicture()

        try:
            #specValue = soup.find_all('div', class_='db-view__item_spec__value')
            specValue = soup.find_all('div', class_='clearfix sys_nq_element')

            # Armor values
            if ("Shield" in slot 
                or "Head" in slot 
                or "Body" in slot 
                or "Hands" in slot
                or "Legs" in slot
                or "Feet" in slot):

                if len(specValue[0].contents) == 5:
                    self.item.defense = int(specValue[0].contents[1].text)
                    self.item.magicDefense = int(specValue[0].contents[3].text)

            # Weapon Values
            elif ("Arm" in slot or "Grimoire" in slot):
                # Healer Weapons
                if ("Conjurer" in slot 
                    or "Scholar" in slot 
                    or "Astrologian" in slot
                    or "Thaumaturge" in slot 
                    or "Arcanist" in slot 
                    or "Red" in slot 
                    or "Blue" in slot):
                    self.item.magicDamage = int(specValue[0].contents[1].text)
                else:
                    # general dps
                    self.item.physicalDamage = int(specValue[0].contents[1].text)

                self.item.autoAttack = float(specValue[0].contents[3].text)
                self.item.delay = float(specValue[0].contents[5].text)
        except Exception as e:
            pass

        self.requiredItems()

        self.jobs()

        # ilevel
        self.iLevel()

        # Materia
        self.materia()

        # Repair Values
        self.repair()

        try:
            itemInfo2 = soup.find_all('ul', class_='db-view__item-info__list')
            self.item.extractable = self.__getItemExtractable__(itemInfo2)
            self.item.projectable = self.__getItemProjectable__(itemInfo2)
            self.item.dyeable = self.__getItemDyeable__(itemInfo2)
            self.item.desynth = self.__getItemDesynthesizable__(itemInfo2)
        except:
            print("Item was missing 'db-view__item-info__list' class")


        self.__getMarketValues__()

        # vendors
        self.__getVendors__()

        # Check if the item contains extra info
        self.instances()

        return self.item

    def __getBonusAttr__(self, htmlResult: Tag ):
        try:
            # Set default values
            self.item.stats = Stats()

            for b in htmlResult[1].contents[5].contents:
                if b == '\n':
                    pass
                elif b.contents[0].text == "Strength":
                    self.item.stats.strength = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Vitality":
                    self.item.stats.vitality = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Mind":
                    self.item.stats.mind = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Intelligence":
                    self.item.stats.intelligence = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Determination":
                    self.item.stats.determination = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Skill Speed":
                    self.item.stats.skillSpeed = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Spell Speed":
                    self.item.stats.spellSpeed = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Dexterity":
                    self.item.stats.dexterity = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == 'Critical Hit':
                    self.item.stats.criticalHit = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Direct Hit Rate":
                    self.item.stats.directHitRate = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Tenacity":
                    self.item.stats.tenacity = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Piety":
                    self.item.stats.piety = self.__cleanBonusAttr__(b.contents[1])
        except Exception as e:
            raise UnableToFindValue("Failed to find BonusAttr, something is missing that is expected.",e)

    def __cleanBonusAttr__(self, value: str) -> int:
        value = value.replace('+', '').replace(' ','')
        return int(value)

    def __parseMateriaValues__(self, materiaCode: ResultSet):
        mslots: int = 0
        try:
            for m in materiaCode[0].contents:
                if m == '\n':
                    pass
                elif m.attrs['class'][1] == 'normal':
                    try:
                        mslots = mslots + 1
                    except:
                        mslots = 1

            self.item.materia.slots = mslots
        except Exception as e:
            raise UnableToFindValue("HTML contained code for MateriaSlots but failed to parse.", e)

    def __getItemExtractable__(self, itemInfo2: ResultSet) -> bool:
        try:
            extractable: bool = False
            html = itemInfo2[0].contents[1]
            key = html.contents[0]
            value = html.contents[1].contents[0]
            if key == 'Extractable: ':
                if value == 'Yes':
                    extractable = True
                
            return extractable
        except:
            UnableToFindValue(
                "Unable to find 'Extractable: ' in the expected location."
                ,f"key: {key}"
                ,f"value: {value}"
            )
            pass

    def __getItemProjectable__(self, itemInfo2: ResultSet) -> bool:
        try:
            projectable: bool = False
            html = itemInfo2[0].contents[1].next_sibling
            if html.contents[0] == 'Projectable: ':
                if html.contents[1].contents[0] == 'Yes':
                    projectable = True

            return projectable
        except:
            raise UnableToFindValue(
                "Unable to find 'Projectable: ' in the expected location."
                ,f"key: {html.contents[0]}"
                ,f"value: {html.contents[1].contents[0]}"
            )

    def __getItemDesynthesizable__(self, itemInfo2: ResultSet) -> float:
        try:
            desynth: float = 0.0
            html = itemInfo2[0].contents[1].next_sibling.next_sibling
            key = html.contents[0]
            value = html.contents[1].contents[0]
            if key == 'Desynthesizable: ':
                if value == 'No':
                    return desynth
                else:
                    desynth = float(value)
            return desynth
        except:
            raise UnableToFindValue()

    def __getItemDyeable__(self, itemInfo2: ResultSet) -> bool:
        try:
            dyeable: bool = False
            html = itemInfo2[0].contents[1].next_sibling.next_sibling.next_sibling
            key = html.contents[0]
            value = html.contents[1].contents[0]
            if key == "Dyeable: ":
                if value == "Yes":
                    dyeable: bool = True
            return dyeable
        except Exception as e:
            raise UnableToFindValue(
            "Unable to find 'Dyeable: ' in the expected location."
            ,f"key: {key}"
            ,f"value: {value}"
            ,f'raw: {e}')

    def getRequiredItems(self, data: ResultSet) -> List:
        try:
            # store all the items and npc's here
            requiredItemsList: List = []

            # this is the core structure
            exchange: ExchangeFor = ExchangeFor()
            #requiredItemsDict: Dict = {'items': [], 'npc': '', 'location': ''}

            items: List = []
            for i in data.contents[0].contents[1]:
                #item: Dict = {'item': '', 'amount': 0}
                item: ExchangeItems = ExchangeItems()
                thin = i.contents[0].next_sibling.contents[0].contents
                item.name = thin[0].text
                item.amount = int(thin[1].text)
                items.append(item)

            #requiredItemsDict['items'] = items
            exchange.items = items

            #requiredItemsDict['npc'] = data.contents[1].text
            exchange.npc = data.contents[1].text

            #requiredItemsDict['location'] = data.contents[2].text
            exchange.location = data.contents[2].text
            return exchange
        except Exception as e:
            print(e)
            pass

    def patchVersion(self) -> None:
        try:
            pPatchVersion = self.soup.find_all('div', class_='db-content db-content__title')
            tpatch = pPatchVersion[0].contents[0].text
            tpatch = tpatch.replace('\n', '')
            tpatch = tpatch.replace('Search ResultsVersion: Patch ', '')
            self.item.patch = tpatch
        except Exception as e:
            print("Unable to find 'patch'. ", e)

    def __getMarketValues__(self) -> None:
        try:
            footer = self.soup.find_all('div', class_='db-view__item_footer')
            if footer != []:
                self.buyPrice = 0
                self.sellPrice = 0
                self.sellOnMarket = True
                self.unsellable = False
                self.item.materia.advancedMelding = True
                # Check for Advanced Melding
                for i in footer[0].contents:
                    if i.text == 'Advanced Melding Forbidden':

                        self.item.materia.advancedMelding = False
                        continue

                    elif 'Available for Purchase:' in i.text:
                        
                        continue
                    
                    elif "Sale Price:" in i.text:
                        textSplit = i.text.split("Sale Price: ")
                        gilSplit = textSplit[1].split(' gil')
                        self.item.vendors.buy = int(gilSplit[0].replace(',',''))
                        continue

                    elif 'Sells for' in i.text:
                        split = i.text.split("Sells for")
                        if len(split) >= 2:
                            for g in split:
                                if 'gil' in g:
                                    gil = g
                                    continue

                        else:
                            gil = split

                        gil = gil.replace(" gil", '')
                        gil = gil.replace(',', '')
                        gil = gil.replace(' ', '')


                        if self.item.vendors.sell != 0:
                            #HQ Item
                            #TODO HQ Sell Price
                            pass
                        else:
                            self.item.vendors.sell = int(gil)
                        continue

                    elif i.text == 'Market Prohibited':
                        self.item.vendors.sellOnMarket = False
                        continue
                    
                    elif i.text == 'Unsellable':
                        self.item.vendors.unsellable = True
                        continue

                    else:
                        print(f"'Market Values' - Found new value '{i}' review.")
        except Exception as e:
            print("Unable to find 'Market Values' results. div = 'db-view__item_footer'", e)
            pass
    
    def __getVendors__(self) -> None:
        try:
            vendors = self.soup.find_all('div', class_='db-shop__npc__space')
            #self.item.buyFrom: List = []
            if vendors != []:                
                vendorRows = vendors[0].contents[0].contents[1].contents
                vendorsList: List = []
                for v in vendorRows:

                    vendors: Vendors = Vendors()

                    name = v.contents[0].contents[0].text
                    loc = v.contents[1].text
                    if name != '' and loc != '':
                        vendors.name = name
                        vendors.location = loc
                        vendorsList.append(vendors)

                self.item.vendors.buyFrom = vendorsList
        except Exception as e:
            print(f"Item did not contain venders", e)

    def instances(self) -> None:
        try:
            htmlBase = self.soup.find_all('div', class_='db__l_main db__l_main__base')
            self.item.relatedDuties = []            
            if htmlBase != []:

                for a in htmlBase:
                    if a == '\n':
                        continue

                    if "Related Duties" in a.contents[1].text:
                        dutiesList: List = []
                        try:
                            #duty: Dict = {'name': '', 'requiredLevel': 0, 'averageItemLevel': 0}
                            duty = DropsFrom()
                            duties = a.contents[3].contents[1].contents[3]
                            duty.type = duties.contents[1].contents[1].contents[1].contents[1].text
                            duty.expansion = duties.contents[1].contents[1].contents[1].contents[3].text
                            duty.name = duties.contents[1].contents[1].contents[3].contents[0]
                            duty.level = int(duties.contents[1].contents[3].text)
                            duty.itemLevel = int(duties.contents[1].contents[5].string)
                            dutiesList.append(duty)

                            self.item.relatedDuties = dutiesList

                        except Exception as e:
                            print("Failed to parse 'Related Duties'", e)
                pass

        except Exception as e:
            pass

    def repair(self) -> None:
        try:
            repair = self.soup.find_all('ul', class_='db-view__item_repair')
            self.item.repair = RepairInfo()
            for r in repair[0].contents:
                if r == '\n':
                    continue

                if r.contents[0].text == "Repair Level":
                    _repair = r.contents[0].next_sibling.text.split(" Lv. ")                    
                    self.item.repair.job = _repair[0]
                    self.item.repair.level = int(_repair[1])
                    continue
                
                if r.contents[0].string == "Materials":
                    self.item.repair.material = r.contents[1].text
                    continue

                if r.contents[0].text == "Materia Melding":
                    _melder = r.contents[1].text.split(' Lv. ')
                    self.item.materia.melderJob = _melder[0]
                    self.item.materia.melderLevel = int(_melder[1])
                    pass

            if "Lv." in repair[0].contents[1].contents[1].text:
                repairBy = repair[0].contents[1].contents[1].contents[0].split(" Lv. ")
                self.item.repair.job: str = repairBy[0]
                self.item.repair.level: int = int(repairBy[1])
                self.item.repair.material: str = repair[0].contents[1].next_sibling.contents[1].contents[0]
        except Exception as e:
            print(f"Unable to find expected HTML for repair values")

    def materia(self) -> None:
        try:
            #materia_ = soup.find_all('div', class_='db-popup__inner')
            materia_ = self.soup.find_all("ul", {'class': 'db-view__materia_socket'})
            self.item.materia = Materia()
            self.item.materia.slots = 0
            self.item.materia.melderJob = ''
            self.item.materia.melderLevel = 0
            if materia_ != []:
                self.__parseMateriaValues__(materia_)
            else:
                self.item.materia.slots = 0
                self.item.materia.melderJob = None
                print(f"{self.item.name} seems to not accept materia.")
        except:
            print(f'Unable to find expected HTML for materia')

    def iLevel(self) -> None:
        try:
            htmlJobLevel = self.soup.find_all('div', {'class': 'db-view__item_equipment__level'})
            if "Lv." in htmlJobLevel[0].text:
                level = htmlJobLevel[0].text.replace("Lv. ", '')
                self.item.level = int(level)
            else:
                self.item.level = 0
        except Exception as e:
            print("Failed to find what level is required for the item.", e)

    def jobs(self) -> None:
        try:
            htmlJobs = self.soup.find_all('div', {'class': "db-view__item_equipment__class"})
            jobsSplit = htmlJobs[0].contents[0].split(' ')
            self.item.jobs = []
            for j in jobsSplit:
                self.item.jobs.append(j)
        except Exception as e:
            print(e)

    def requiredItems(self) -> None:
        try:
            bonusAttr = self.soup.find_all('div', class_='sys_nq_element')

            # Bonus Stats
            self.__getBonusAttr__(bonusAttr)

            self.item.requiredItems = []
            if "Required Items" in bonusAttr[2].contents[0].text:
                requiredItemsList: List = []

                for ri in bonusAttr[2].contents:
                    if ri.text == "Required Items":
                        continue

                    if ri.contents[0].attrs['class'][0] == 'db-shop__item':
                        requiredItemsList.append(self.getRequiredItems(ri))
                    
                self.item.requiredItems = requiredItemsList
        except:
            print("Unable to find 'div class='sys_nq_element'.  Could be expected result based on the item.")
            #raise UnableToFindValue("Unable to find 'div class='sys_nq_element'")

    def itemPicture(self) -> None:
        try:
            pictureUrl = self.soup.find_all('div', class_='db-view__item__icon latest_patch__major__detail__item')
            try:
                for p in pictureUrl[0].contents:
                    if p == '\n':
                        continue

                    if p.attrs['class'][0] == 'latest_patch__major__icon':
                        continue

                    if p.attrs['class'][0] == "staining":
                        continue

                    elif p.attrs['class'][0] == 'db-view__item__icon__cover':
                        continue

                    elif p.attrs['width'] == '152':
                        continue

                    elif p.attrs['width'] == '128':
                        self.item.pictureUrl = p.attrs['src']
                        self.item.pictureWidth = int(p.attrs['width'])
                        self.item.pictureHeight = int(p.attrs['height'])
                    else:
                        print("new values found in pictureUrl")
            except Exception as e:
                print("Error parsing pictureUrl", e)
        except Exception as e:
            raise UnableToFindValue("msg: Unable to find a 'div' with class 'db-view__item__icon latest_patch__major__detail__item'")
